import re

from .base import Base
from ..utils import utils
from ..utils import constants as EC


class Promoter(Base):
    def __init__(self, **kwargs):
        super(Promoter, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.minus_10_left = kwargs.get("minus_10_left", None)
        self.minus_10_right = kwargs.get("minus_10_right", None)
        self.minus_35_left = kwargs.get("minus_35_left", None)
        self.minus_35_right = kwargs.get("minus_35_right", None)
        self.modified_id = kwargs.get("modified_id", None)
        self.pos1 = kwargs.get("absolute_plus_1_pos", None)
        self.sequence = kwargs.get("sequence", None)
        self.binding_sigma_factor = kwargs.get("binding_sigma_factor", None)
        self.score = kwargs.get("score", None)
        self.transcription_start_site = kwargs.get("absolute_plus_1_pos", None)
        self.distance_to_gene = kwargs.get("distance_to_gene", None)

    @property
    def db_links(self):
        return self._db_links

    @db_links.setter
    def db_links(self, db_links):
        self._db_links = []
        try:
            self._db_links.extend(
                utils.get_external_cross_references(db_links))
        except TypeError:
            pass

        ecocyc_reference = {
            "externalCrossReferences_id": "|ECOCYC|",
            "objectId": self.id.replace("|", ""),
        }
        self._db_links.append(ecocyc_reference.copy())

        if self.bnumber:
            bnumber_reference = {
                "externalCrossReferences_id": "|REFSEQ|",
                "objectId": self.bnumber,
            }
            self._db_links.append(bnumber_reference.copy())

    @property
    def distance_to_gene(self):
        return self._distance_to_gene

    @distance_to_gene.setter
    def distance_to_gene(self, distance_to_gene):
        self._distance_to_gene = []
        absolute_pos = self.pos1
        if absolute_pos is None:
            absolute_pos = self.transcription_start_site
        if absolute_pos:
            for minus_box in [
                (self.minus_10_left, self.minus_10_right, "minus10"),
                (self.minus_35_left, self.minus_35_right, "minus35"),
            ]:
                if minus_box[0] and minus_box[1]:
                    if self.strand == "reverse":
                        minus = {
                            "distance": (minus_box[1] - absolute_pos),
                            "type": minus_box[2]
                        }
                        self._distance_to_gene.append(minus)

                    elif self.strand == "forward":
                        minus = {
                            "distance": (absolute_pos - minus_box[0]),
                            "type": minus_box[2]
                        }
                        self._distance_to_gene.append(minus)

                    else:
                        self._distance_to_gene = []

    @property
    def binds_sigma_factor(self):
        return self._binding_sigma_factor

    @property
    def modified_id(self):
        return self._modified_id

    @modified_id.setter
    def modified_id(self, modified_id=None):
        self._modified_id = modified_id

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence=None):
        if sequence is None:
            if self.strand is not None and self.pos1 is not None:
                if self.strand.lower() == "reverse":
                    initial_position = self.pos1 - (self._offset * 0.25)
                    end_position = self.pos1 + (self._offset * 0.75)
                    sequence = self.pt_connection.get_sequence(
                        initial_position, end_position, "X"
                    )
                    sequence = self.pt_connection.get_reverse_complement(
                        sequence)
                else:
                    initial_position = self.pos1 - (self._offset * 0.75)
                    end_position = self.pos1 + (self._offset * 0.25)
                    sequence = self.pt_connection.get_sequence(
                        initial_position, end_position, "X"
                    )
                initial = int(self._offset * 0.75)
                last = int(self._offset * 0.25)
                sequence = (
                    sequence[:initial].lower()
                    + sequence[initial: initial + 1]
                    + sequence[-last:].lower()
                )

                self._sequence = sequence
            else:
                self._sequence = None
        else:
            self._sequence = sequence

    @property
    def transcription_start_site(self):
        return self._transcription_start_site

    @transcription_start_site.setter
    def transcription_start_site(self, pos1):
        if pos1 is not None:
            try:
                # Since promoters do not have left end position and right end position
                # the range is of 1 nucleotide (up to pathway tools 24.0)
                range_ = 1
                transcription_start_site = {
                    "leftEndPosition": pos1,
                    "rightEndPosition": pos1,
                    "range": range_,
                }
                transcription_start_site = {
                    k: v for k, v in transcription_start_site.items() if v is not None
                }
            except TypeError:
                transcription_start_site = None
            self._transcription_start_site = transcription_start_site
        else:
            self._transcription_start_site = None

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score=None):
        if score is None:
            score = self.get_score(self.comment)
        if score:
            self._score = score
        else:
            self._score = None

    @staticmethod
    def get_score(comment):
        format_value = "%.2f"
        score = None
        # We obtain the score through the comment from the promoter object
        # in order to accomplish this with need to use a regex
        if comment is not None:
            match = re.search(r"Score:\s?(-?\d+\.\d+)\.", comment)
            # if the regex match with the note (promoter's comment)
            # then we obtain the result and format it.
            try:
                score = float(format_value % float(match.group(1)))
            except AttributeError:
                score = None
        return score

    @property
    def binding_sigma_factor(self):
        return self._binding_sigma_factor

    @binding_sigma_factor.setter
    def binding_sigma_factor(self, binding_sigma_factor=None):
        try:
            sigma_factor_id = binding_sigma_factor[0]
            citations = Promoter.citations_binding_sigma_factor(
                self.id, sigma_factor_id
            )
            binding_sigma_factor = {
                "sigmaFactors_id": sigma_factor_id,
                "citations": citations,
            }
            binding_sigma_factor = self.get_only_properties_with_values(
                binding_sigma_factor
            )
            if binding_sigma_factor:
                self._binding_sigma_factor = binding_sigma_factor
            else:
                self._binding_sigma_factor = None
        except TypeError:
            self._binding_sigma_factor = None

    @staticmethod
    def citations_binding_sigma_factor(promoter_feature_id, sigma_factor_id):
        citations = Promoter.pt_connection.get_value_annot_list(
            promoter_feature_id,
            EC.BINDS_SIGMA_FACTOR_SLOT,
            sigma_factor_id,
            EC.CITATIONS_SLOT,
        )
        citations = utils.get_citations(citations)
        return citations

    def get_promoter_boxes(self, minus_signals=None):
        if minus_signals is None:
            minus_signals = []
            for minus_box in [
                (self.minus_10_left, self.minus_10_right, "minus10"),
                (self.minus_35_left, self.minus_35_right, "minus35"),
            ]:
                if minus_box[0] or minus_box[1]:
                    minus_signal = dict(
                        leftEndPosition=minus_box[0],
                        rightEndPosition=minus_box[1],
                        sequence=Base.get_sequence(
                            minus_box[0], minus_box[1], self.strand
                        ),
                        type=minus_box[2],
                    )
                    minus_signal = {
                        k: v for k, v in minus_signal.items() if v is not None
                    }
                    if minus_signal not in minus_signals:
                        minus_signals.append(minus_signal.copy())
            if not minus_signals:
                minus_signals = None
        return minus_signals
