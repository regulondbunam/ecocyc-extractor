from .base import Base
from ..utils import constants as EC
from ..utils import utils


class TranscriptionFactorRegulatorySite(Base):
    def __init__(self, **kwargs):
        super(TranscriptionFactorRegulatorySite, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.absolute_position = kwargs.get("absolute_position", None)
        self.length = kwargs.get("length", None)
        self.left_end_position = kwargs.get("lend", None)
        self.right_end_position = kwargs.get("rend", None)
        self.sequence = kwargs.get("sequence", None)
        self.regulatory_interaction_ids = kwargs.get(
            "involved_in_regulation", None)
        self.mechanism = kwargs.get("mechanism", None)

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

    def to_dict(self):
        site = dict(
            _id=self.id,
            absolutePosition=self.absolute_position,
            citations=self.citations,
            externalCrossReferences=self.db_links,
            internalComment=self.internal_comment,
            involved_in_regulation=self.regulatory_interaction_ids,
            leftEndPosition=self.left_end_position,
            length=self.length,
            note=self.comment,
            rightEndPosition=self.right_end_position,
            sequence=self.sequence,
        )
        site = self.get_only_properties_with_values(site)
        return site

    @property
    def left_end_position(self):
        if self._left_end_position == self._right_end_position:
            self._left_end_position = None
            self._right_end_position = None
        return self._left_end_position

    @left_end_position.setter
    def left_end_position(self, lend=None):
        if lend is None:
            lend = self.pt_connection.get_site_left_position_extended(self.id)
        self._left_end_position = lend

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length=None):
        if length is None:
            length = self.pt_connection.binding_site_size(self.id)
        self._length = length

    @property
    def right_end_position(self):
        if self._left_end_position == self._right_end_position:
            self._right_end_position = None
            self._left_end_position = None
        return self._right_end_position

    @right_end_position.setter
    def right_end_position(self, rend=None):
        if rend is None:
            rend = self.pt_connection.get_site_right_position_extended(self.id)
        self._right_end_position = rend

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence=None, strand=None, offset=10):
        """

        :param sequence:
        :param strand:
        :param offset:
        :return:
        """
        if sequence is None and strand is not None:
            try:
                # if both positions have identical values then it means that there's an inconsistency
                # on the site positions' data or pathway tool's functions
                if self.left_end_position == self.right_end_position:
                    sequence = None
                else:
                    sequence = Base.get_sequence(
                        self.left_end_position, self.right_end_position, strand, offset
                    )
            except TypeError:
                self._sequence = None
        self._sequence = sequence

    @property
    def mechanism(self):
        return self._mechanism

    @mechanism.setter
    def mechanism(self, mechanism):
        regulatory_interaction_id = self.pt_connection.get_slot_value(
            self.id, EC.INVOLVED_IN_REGULATION)
        all_parents = self.pt_connection.get_frame_all_parents(
            regulatory_interaction_id)
        if EC.REGULATION_OF_TRANSLATION in all_parents:
            self._mechanism = "Translation"
        elif EC.REGULATION_OF_TRANSCRIPTION in all_parents:
            self._mechanism = "Transcription"
        else:
            self._mechanism = "Unknown"
