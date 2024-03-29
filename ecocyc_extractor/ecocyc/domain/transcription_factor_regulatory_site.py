from .base import Base
from ..utils import constants as EC
from ..utils import utils


class TranscriptionFactorRegulatorySite(Base):
    MINUS_N_POS = 1

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
        self.regulation_type = kwargs.get("regulation_type", None)

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
        if rend is not None:
            rend = rend - TranscriptionFactorRegulatorySite.MINUS_N_POS
            # Se resta una position para que concida con los datos de RegulonDB
        self._right_end_position = rend

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence=None, strand="forward", offset=10):
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
                if not self.length:
                    sequence = None
                else:
                    if self.left_end_position == self.right_end_position:
                        sequence = None
                    elif self.left_end_position is None or self.right_end_position is None:
                        sequence = None
                    else:
                        sequence = Base.get_sequence(
                            self.left_end_position, self.right_end_position, strand, offset)
            except TypeError:
                self._sequence = None
        self._sequence = sequence

    @property
    def regulation_type(self):
        return self._regulation_level

    @regulation_type.setter
    def regulation_type(self, regulation_type):
        regulatory_interaction_id = self.pt_connection.get_slot_value(
            self.id, EC.INVOLVED_IN_REGULATION)
        all_parents = self.pt_connection.get_frame_all_parents(
            regulatory_interaction_id)
        if EC.RNA_MEDIATED_TRANSLATION_REGULATION in all_parents:
            self._regulation_level = "sRNA-Regulation"
        elif EC.PROTEIN_MEDIATED_TRANSLATION_REGULATION in all_parents:
            self._regulation_level = "Protein-Regulation"
        elif EC.REGULATION_OF_TRANSCRIPTION in all_parents:
            self._regulation_level = "Transcription"
        else:
            self._regulation_level = "Unknown"
