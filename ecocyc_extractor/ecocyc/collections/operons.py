import logging

from ecocyc.utils.pathway_tools.connection import Connection
from ecocyc.domain.operon import Operon
from ..utils import constants as EC


class Operons(object):

    pt_connection = Connection()

    def __init__(self):
        self.operons = Operons.get_operons()

    @staticmethod
    def get_operons():
        operons = Operons.pt_connection.all_operons()
        return operons

    @property
    def objects(self):
        for operon in self.operons:
            operon = Operons.set_operon(operon)
            logging.info("Working on operon: {}".format(operon["id"]))
            ecocyc_operon = Operon(**operon)
            yield ecocyc_operon

    @staticmethod
    def set_operon(operon):
        new_operon = dict(
            id=operon,
            dblinks=EC.DBLINKS,
            organism=EC.ORGANISM_ID,
            transcription_unit_ids=operon,
        )
        return new_operon
