import logging

from ecocyc.utils.pathway_tools.connection import Connection
from ecocyc.utils import constants as EC, utils
from ecocyc.domain.cryptic_prophage import CrypticProphage


class CrypticProphages(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = CrypticProphages.get_ids(ids)

    @staticmethod
    def get_ids(ids=None):
        if ids is None:
            cryptic_prophages_ids = CrypticProphages.pt_connection.get_class_all_instances(EC.CRYPTIC_PROPHAGES)
        else:
            cryptic_prophages_ids = ids
        cryptic_prophages_ids = utils.get_unique_elements(cryptic_prophages_ids)
        return cryptic_prophages_ids

    @property
    def objects(self):
        cryptic_prophages_objects = CrypticProphages.pt_connection.get_frame_objects(self.ids)
        for raw_prophage in cryptic_prophages_objects:
            prophage = CrypticProphages.set_cryptic_prophage(raw_prophage)
            logging.info('Working on promoter: {}'.format(prophage["id"]))
            ecocyc_prophage = CrypticProphage(**prophage)
            yield ecocyc_prophage

    @staticmethod
    def set_cryptic_prophage(cryptic_prophage):
        new_cryptic_prophage = dict(
            id=cryptic_prophage[EC.ID],
            citations=cryptic_prophage[EC.CITATIONS],
            dblinks=cryptic_prophage[EC.DBLINKS],
            name=cryptic_prophage[EC.NAME],
            lend=cryptic_prophage[EC.LEND],
            rend=cryptic_prophage[EC.REND],
            strand=cryptic_prophage[EC.TRANSCRIPTION_DIRECTION],
            synonyms=cryptic_prophage[EC.SYNONYMS]
        )
        return new_cryptic_prophage
