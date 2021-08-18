import logging

from ecocyc.utils.pathway_tools.connection import Connection
from ecocyc.utils import constants as EC, utils
from ecocyc.domain.transcription_unit import TranscriptionUnit


class TranscriptionUnits(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = TranscriptionUnits.get_ids(ids)

    @staticmethod
    def get_ids(transcription_unit_ids=None):
        if transcription_unit_ids is None:
            transcription_unit_ids = TranscriptionUnits.pt_connection.get_class_all_instances(EC.TRANSCRIPTION_UNIT_CLASS)
        transcription_unit_ids = utils.get_unique_elements(transcription_unit_ids)
        return transcription_unit_ids

    @property
    def objects(self):
        transcription_unit_objects = TranscriptionUnits.pt_connection.get_frame_objects(self.ids)
        for transcription_unit in transcription_unit_objects:
            transcription_unit = TranscriptionUnits.set_transcription_unit(transcription_unit)
            logging.info('Working on transcription unit: {}'.format(transcription_unit["id"]))
            ecocyc_transcription_unit = TranscriptionUnit(**transcription_unit)
            yield ecocyc_transcription_unit

    @staticmethod
    def set_transcription_unit(transcription_unit):
        new_transcription_unit = dict(
            id=transcription_unit[EC.ID],
            citations=transcription_unit[EC.CITATIONS],
            comment=transcription_unit[EC.COMMENT],
            dblinks=transcription_unit[EC.DBLINKS],
            internal_comment=transcription_unit[EC.INTERNAL_COMMENT],
            name=transcription_unit[EC.NAME],
            organism=EC.ORGANISM_ID,
            synonyms=transcription_unit[EC.SYNONYMS]
        )
        return new_transcription_unit
