import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.sigma_factor import SigmaFactor


class SigmaFactors(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = self.get_ids(ids)

    @staticmethod
    def get_ids(ids=None):
        if ids is None:
            sigma_factor_ids = SigmaFactors.pt_connection.all_sigma_factors()
        else:
            sigma_factor_ids = ids
        sigma_factor_ids = utils.get_unique_elements(sigma_factor_ids)
        return sigma_factor_ids

    @property
    def objects(self):
        sigma_factor_objects = SigmaFactors.pt_connection.get_frame_objects(
            self.ids)
        for sigma_factor in sigma_factor_objects:
            sigma_factor = SigmaFactors.set_sigma_factor(sigma_factor)
            logging.info('Working on sigma factor: {}'.format(
                sigma_factor["id"]))
            ecocyc_sigma_factor = SigmaFactor(**sigma_factor)
            yield ecocyc_sigma_factor

    @staticmethod
    def set_sigma_factor(sigma_factor):
        new_sigma_factor = dict(
            id=sigma_factor[EC.ID],
            abbreviated_name=sigma_factor[EC.ABBREV_NAME],
            citations=sigma_factor[EC.CITATIONS],
            comment=sigma_factor[EC.COMMENT],
            dblinks=sigma_factor[EC.DBLINKS],
            gene=sigma_factor[EC.GENE],
            internal_comment=sigma_factor[EC.INTERNAL_COMMENT],
            name=sigma_factor[EC.NAME],
            organism=EC.ORGANISM_ID,
            synonyms=sigma_factor[EC.SYNONYMS]
        )
        return new_sigma_factor
