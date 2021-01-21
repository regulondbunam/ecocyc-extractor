import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.promoter import Promoter


class Promoters(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = self.get_ids(ids)

    @staticmethod
    def get_ids(ids=None):
        if ids is None:
            promoter_ids = Promoters.pt_connection.get_class_all_instances(
                EC.PROMOTER_CLASS
            )
        else:
            promoter_ids = ids
        promoter_ids = utils.get_unique_elements(promoter_ids)
        return promoter_ids

    @property
    def objects(self):
        promoter_objects = Promoters.pt_connection.get_frame_objects(self.ids)
        for raw_promoter in promoter_objects:
            promoter = Promoters.set_promoter(raw_promoter)
            logging.info("Working on promoter: {}".format(promoter["id"]))
            ecocyc_promoter = Promoter(**promoter)
            yield ecocyc_promoter

    @staticmethod
    def set_promoter(promoter):
        new_promoter = dict(
            id=promoter[EC.ID],
            absolute_plus_1_pos=promoter[EC.ABSOLUTE_PLUS_1_POS],
            binding_sigma_factor=promoter[EC.BINDS_SIGMA_FACTOR_SLOT],
            citations=promoter[EC.CITATIONS],
            comment=promoter[EC.COMMENT],
            dblinks=promoter[EC.DBLINKS],
            internal_comment=promoter[EC.INTERNAL_COMMENT],
            name=promoter[EC.NAME],
            minus_10_left=promoter[EC.MINUS_10_LEFT],
            minus_10_right=promoter[EC.MINUS_10_RIGHT],
            minus_35_left=promoter[EC.MINUS_35_LEFT],
            minus_35_right=promoter[EC.MINUS_35_RIGHT],
            offset=80,
            organism=EC.ORGANISM_ID,
            score=promoter[EC.SCORE],
            strand=promoter[EC.TRANSCRIPTION_DIRECTION],
            synonyms=promoter[EC.SYNONYMS],
        )
        return new_promoter
