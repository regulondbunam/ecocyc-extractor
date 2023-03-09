import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.regulatory_complex import RegulatoryComplex
from ecocyc_extractor.ecocyc.collections.regulatory_interactions import RegulatoryInteractions
from ecocyc_extractor.ecocyc.collections.transcription_factors import TranscriptionFactors
from ecocyc_extractor.ecocyc.domain.transcription_factor import TranscriptionFactor


class RegulatoryComplexes(object):

    pt_connection = Connection()
    product_ids = RegulatoryComplex.product_ids
    compounds_ids = RegulatoryComplex.compound_ids
    regulatory_interaction_ids = RegulatoryInteractions.get_ids()
    transcription_factor_ids = TranscriptionFactors.get_ids()

    def __init__(self, ids=None, include_inactive=False):
        self.ids = RegulatoryComplexes.get_ids(ids, include_inactive)

    @staticmethod
    def get_ids(ids=None, include_inactive=True):
        if ids is None:
            regulator_ids = RegulatoryComplexes.get_regulator_ids(
                RegulatoryComplexes.regulatory_interaction_ids)
            regulatory_complex_ids = RegulatoryComplexes.get_protein_cplx_ids_from_regulators(regulator_ids)
            if include_inactive is True:
                for tf_id in RegulatoryComplexes.transcription_factor_ids:
                    inactive_conformation_ids = TranscriptionFactor.get_tf_inactive_conformations(tf_id)
                    regulatory_complex_ids.extend(inactive_conformation_ids)
        else:
            regulatory_complex_ids = ids
        regulatory_complex_ids = utils.get_unique_elements(regulatory_complex_ids)
        return regulatory_complex_ids

    @property
    def objects(self):
        regulatory_complex_objects = RegulatoryComplexes.pt_connection.get_frame_objects(self.ids)
        for regulatory_complex in regulatory_complex_objects:
            regulatory_complex = RegulatoryComplexes.set_regulatory_complex(regulatory_complex)
            logging.info('Working on regulatory complex: {}'.format(regulatory_complex["id"]))
            ecocyc_regulatory_complex = RegulatoryComplex(**regulatory_complex)
            yield ecocyc_regulatory_complex

    @staticmethod
    def set_regulatory_complex(regulatory_complex):
        new_regulatory_complex = dict(
            id=regulatory_complex[EC.ID],
            abbreviated_name=regulatory_complex[EC.ABBREV_NAME],
            comment=regulatory_complex[EC.COMMENT],
            components=regulatory_complex[EC.COMPONENTS],
            dblinks=regulatory_complex[EC.DBLINKS],
            internal_comment=regulatory_complex[EC.INTERNAL_COMMENT],
            name=regulatory_complex[EC.NAME],
            organism=EC.ORGANISM_ID,
            regulates=regulatory_complex[EC.REGULATES],
            unmodified_form=regulatory_complex[EC.UNMODIFIED_FORM]
        )
        return new_regulatory_complex

    @staticmethod
    def get_protein_cplx_ids_from_regulators(regulator_ids):
        regulatory_complex_ids = []
        for regulator in regulator_ids:
            if regulator is not None:
                if regulator not in RegulatoryComplexes.product_ids and regulator not in RegulatoryComplexes.compounds_ids:
                    regulatory_complex_ids.append(regulator)
        regulatory_complex_ids = utils.get_unique_elements(regulatory_complex_ids)
        return regulatory_complex_ids

    @staticmethod
    def get_regulator_ids(regulatory_interaction_ids):
        regulator_ids = []
        for ri_id in regulatory_interaction_ids:
            regulator_id = RegulatoryComplexes.pt_connection.get_slot_value(ri_id, EC.REGULATOR_SLOT)
            if regulator_id:
                regulator_ids.append(regulator_id)
        regulator_ids = utils.get_unique_elements(regulator_ids)
        return regulator_ids
