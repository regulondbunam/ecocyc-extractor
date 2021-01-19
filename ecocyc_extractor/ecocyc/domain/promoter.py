import re

from .base import Base
from ..utils import utils
from ..utils import constants as EC


class Promoter(Base):

    def __init__(self, **kwargs): #keyword arguments
        super(Promoter, self).__init__(**kwargs)
        self.modified_id = kwargs.get("modified_id", None)
        self.pos1 = kwargs.get("absolute_plus_1_pos", None)
        self.sequence = kwargs.get("sequence", None)
        self.sigma_factor = kwargs.get("sigma_factor", None)
        self.transcription_start_site = kwargs.get("transcription_start_site", None)
        self.promoter_boxes = kwargs.get("promoter_boxes", None)

    @property
    def modified_id(self):
        return self._modified_id

    @modified_id.setter
    def modified_id(self, modified_id=None):
        self._modified_id = modified_id

    @property
    def promoter_boxes(self):
        return self._promoter_boxes

    @promoter_boxes.setter
    def promoter_boxes(self, promoter_boxes=None):
        if promoter_boxes is not None:
            self._promoter_boxes = self.get_promoter_boxes(promoter_boxes, self.get_score(self.comment), self.sigma_factor, self.strand)
        else:
            self._promoter_boxes = None

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
                    sequence = self.pt_connection.get_sequence(initial_position, end_position, "X")
                    sequence = self.pt_connection.get_reverse_complement(sequence)
                else:
                    initial_position = self.pos1 - (self._offset * 0.75)
                    end_position = self.pos1 + (self._offset * 0.25)
                    sequence = self.pt_connection.get_sequence(initial_position, end_position, "X")
                initial = int(self._offset * 0.75)
                last = int(self._offset * 0.25)
                sequence = sequence[:initial].lower() + sequence[initial:initial + 1] + sequence[-last:].lower()

                self._sequence = sequence
            else:
                self._sequence = None
        else:
            self._sequence = sequence

    @property
    def sigma_factor(self):
        return self._sigma_factor

    @sigma_factor.setter
    def sigma_factor(self, sigma_factor=None):
        if sigma_factor is None:
            sigma_factor = self.pt_connection.get_promoter_sigma_factor(self.id)
        if sigma_factor:
            self._sigma_factor = sigma_factor
        else:
            self._sigma_factor = None

    @property
    def transcription_start_site(self):
        return self._transcription_start_site

    @transcription_start_site.setter
    def transcription_start_site(self, transcription_start_site=None):
        if transcription_start_site is None:
            try:
                # Since promoters do not have left end position and right end position
                # the range is of 1 nucleotide (up to pathway tools 24.0)
                range_ = 1
                transcription_start_site = {
                    "leftEndPosition": int(self.pos1),
                    "rightEndPosition": int(self.pos1),
                    "range": range_
                }
                transcription_start_site = {k: v for k, v in transcription_start_site.items() if v is not None}
            except TypeError:
                transcription_start_site = None
        self._transcription_start_site = transcription_start_site

    @staticmethod
    def get_score(comment):
        format_value = "%.2f"
        score = None
        # We obtain the score through the comment from the promoter object
        # in order to accomplish this with need to use a regex
        if comment is not None:
            match = re.search(r'Score:\s?(-?\d+\.\d+)\.', comment)
            # if the regex match with the note (promoter's comment)
            # then we obtain the result and format it.
            try:
                score = float(format_value % float(match.group(1)))
            except AttributeError:
                score = None
        return score

    @staticmethod
    def get_promoter_boxes(promoter_boxes, score, sigma_factor, strand):
        promoter_properties = {
            "score_promoter": score,
            "sigma_factor_promoter": sigma_factor,
            "strand_promoter": strand,
        }
        new_promoter_boxes = []
        # pt_promoter_boxes = pathway tools promoter boxes a.k.a. promoter boxes from the current loaded db
        pt_promoter_boxes = Promoter.pt_connection.get_frame_objects(promoter_boxes)
        for pt_promoter_box in pt_promoter_boxes:
            pt_promoter_box = Promoter.set_promoter_box(pt_promoter_box, promoter_properties)
            regulondb_promoter_feature = PromoterFeature(**pt_promoter_box)
            regulondb_promoter_feature = regulondb_promoter_feature.to_dict()
            if regulondb_promoter_feature is not None:
                if regulondb_promoter_feature not in new_promoter_boxes:
                    new_promoter_boxes.append(regulondb_promoter_feature)
        return new_promoter_boxes

    @staticmethod
    def set_promoter_box(promoter_box, promoter_properties):
        new_promoter_box = dict(
            id=promoter_box[EC.ID],
            binds_sigma_factor=promoter_box[EC.BINDS_SIGMA_FACTOR],
            citations=promoter_box[EC.CITATIONS],
            minus_10_left=promoter_box[EC.MINUS_10_LEFT],
            minus_10_right=promoter_box[EC.MINUS_10_RIGHT],
            minus_35_left=promoter_box[EC.MINUS_35_LEFT],
            minus_35_right=promoter_box[EC.MINUS_35_RIGHT],
            score=promoter_properties.get("score_promoter", None),
            sigma_factor_promoter=promoter_properties.get("sigma_factor_promoter", None),
            strand=promoter_properties.get("strand_promoter", None)
        )
        return new_promoter_box


class PromoterFeature(Base):

    def __init__(self, **kwargs):
        super(PromoterFeature, self).__init__(**kwargs)
        self.binds_sigma_factor = kwargs.get("binds_sigma_factor", None)
        self.minus_10_left = kwargs.get("minus_10_left", None)
        self.minus_10_right = kwargs.get("minus_10_right", None)
        self.minus_35_left = kwargs.get("minus_35_left", None)
        self.minus_35_right = kwargs.get("minus_35_right", None)
        self.minus_signals = kwargs.get("minus_signals", None)
        self.score = kwargs.get("score", None)
        self.sigma_factor_promoter = kwargs.get("sigma_factor_promoter", None)

    @property
    def binds_sigma_factor(self):
        return self._binds_sigma_factor

    @binds_sigma_factor.setter
    def binds_sigma_factor(self, binds_sigma_factor=None):
        try:
            sigma_factor_id = binds_sigma_factor[0]
            citations = PromoterFeature.citations_binds_sigma_factor(self.id, sigma_factor_id)
            binds_sigma_factor = {
                "sigmaFactors_id": sigma_factor_id,
                "citations": citations
            }
            binds_sigma_factor = self.get_only_properties_with_values(binds_sigma_factor)
            if binds_sigma_factor:
                self._binds_sigma_factor = binds_sigma_factor
            else:
                self._binds_sigma_factor = None
        except TypeError:
            self._binds_sigma_factor = None

    @staticmethod
    def citations_binds_sigma_factor(promoter_feature_id, sigma_factor_id):
        citations = PromoterFeature.pt_connection.get_value_annot_list(promoter_feature_id, EC.BINDS_SIGMA_FACTOR_SLOT, sigma_factor_id, EC.CITATIONS_SLOT)
        citations = utils.get_citations(citations)
        return citations

    def to_dict(self):
        promoter_box = {}
        if self.binds_sigma_factor is not None:
            if self.binds_sigma_factor["sigmaFactors_id"] == self.sigma_factor_promoter:
                promoter_box = dict(
                    promoterFeature_id=self.id,
                    citations=self.citations,
                    score=self.score,
                    bindsSigmaFactor=self.binds_sigma_factor,
                    boxes=self.minus_signals
                )
        elif self.sigma_factor_promoter is None:
            promoter_box = dict(
                promoterFeature_id=self.id,
                citations=self.citations,
                score=self.score,
                boxes=self.minus_signals
            )

        promoter_box = {k: v for k, v in promoter_box.items() if v is not None}

        return promoter_box

    @property
    def minus_signals(self):
        return self._minus_signals

    @minus_signals.setter
    def minus_signals(self, minus_signals=None):
        if minus_signals is None:
            minus_signals = []
            for minus_box in [(self.minus_10_left, self.minus_10_right, "minus10"), (self.minus_35_left, self.minus_35_right, "minus35")]:
                if minus_box[0] or minus_box[1]:
                    minus_signal = dict(
                        leftEndPosition=minus_box[0],
                        rightEndPosition=minus_box[1],
                        sequence=Base.get_sequence(minus_box[0], minus_box[1], self.strand),
                        type=minus_box[2]
                    )
                    minus_signal = {k: v for k, v in minus_signal.items() if v is not None}
                    if minus_signal not in minus_signals:
                        minus_signals.append(minus_signal.copy())
            if not minus_signals:
                minus_signals = None
        self._minus_signals = minus_signals
