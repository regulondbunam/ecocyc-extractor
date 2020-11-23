import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC
from ecocyc_extractor.ecocyc.domain.transcription_factor import TranscriptionFactor
from ecocyc_extractor.ecocyc.collections.regulatory_interactions import RegulatoryInteractions


class TranscriptionFactors(object):
    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = self.get_ids(ids)

    @staticmethod
    def get_ids(transcription_factor_ids=None):
        if transcription_factor_ids is None:
            transcription_factor_ids = TranscriptionFactors.get_transcription_factor_ids()
        return transcription_factor_ids

    @property
    def objects(self):
        transcription_factor_objects = self.pt_connection.get_frame_objects(self.ids)
        for transcription_factor in transcription_factor_objects:
            transcription_factor = TranscriptionFactors.set_transcription_factor(transcription_factor)
            logging.info('Working on transcription factor: {}'.format(transcription_factor["id"]))
            ecocyc_transcription_factor = TranscriptionFactor(**transcription_factor)
            yield ecocyc_transcription_factor

    @staticmethod
    def set_transcription_factor(transcription_factor):

        new_transcription_factor = dict(
            id=transcription_factor[EC.ID],
            abbreviated_name=transcription_factor[EC.ABBREV_NAME],
            citations=transcription_factor[EC.CITATIONS],
            comment=transcription_factor[EC.COMMENT],
            dblinks=transcription_factor[EC.DBLINKS],
            internal_comment=transcription_factor[EC.INTERNAL_COMMENT],
            name=transcription_factor[EC.NAME],
            organism=EC.ORGANISM_ID,
            site_length=transcription_factor[EC.SITE_LENGTH],
            synonyms=transcription_factor[EC.SYNONYMS]
        )

        return new_transcription_factor

    @staticmethod
    def get_transcription_factor_ids():
        """

        :return:
        """
        ri_ids = RegulatoryInteractions.get_ids(transcription_factors_ris=True)
        transcription_factor_ids = []
        regulator_ids = TranscriptionFactors.get_regulator_ids(ri_ids)
        for regulator_id in regulator_ids:
            monomer_ids = TranscriptionFactors.pt_connection.monomers_of_protein(regulator_id, unmodify=True)

            regulator_classes = TranscriptionFactor.pt_connection.get_frame_all_parents(regulator_id)

            if not monomer_ids and EC.COMPOUNDS_CLASS not in regulator_classes:
                transcription_factor_ids.append(regulator_id)
            if len(monomer_ids) == 1:
                transcription_factor_ids.append(monomer_ids[0])
            elif len(monomer_ids) > 1:
                # For those TFs that are protein dimers, that is to say, that is formed through two different
                # polypeptides we save the protein complex(dimer) and store it as a TF, they will be seen in the
                # regulatory complexes collection in the property isTranscriptionFactor = True
                transcription_factor_ids.append(regulator_id)
        return transcription_factor_ids


    @staticmethod
    def get_regulator_ids(ri_ids):
        regulator_ids = []
        for ri_id in ri_ids:
            regulator = TranscriptionFactors.pt_connection.get_slot_value(ri_id, EC.REGULATOR_SLOT)
            if regulator:
                regulator_ids.append(regulator)

        regulator_ids = list(set(regulator_ids))
        return regulator_ids
