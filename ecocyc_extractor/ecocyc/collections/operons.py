"""
Operons collection
"""
# standard
import logging

# third party

# local
from ..utils.pathway_tools.connection import Connection
from ..domain.operon import Operon
from ..utils import constants as EC
from ..utils.utils import print_progress


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
        total_objects = len(list(self.operons))
        processed = 0
        for operon in self.operons:
            operon = Operons.set_operon(operon)
            logging.info("Working on operon: {}".format(operon["id"]))
            ecocyc_operon = Operon(**operon)
            processed += 1
            print_progress(
                current=processed,
                total=total_objects,
                collection_name="Operons"
            )
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
