import logging

from ecocyc.utils.pathway_tools.connection import Connection
from ecocyc.utils import constants as EC, utils
from ecocyc.domain.terminator import Terminator


class Terminators(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = self.get_ids(ids)

    @staticmethod
    def get_ids(ids=None):
        if ids is None:
            terminator_ids = Terminators.pt_connection.get_class_all_instances(EC.TERMINATOR_CLASS)
        else:
            terminator_ids = ids
        terminator_ids = utils.get_unique_elements(terminator_ids)
        return terminator_ids

    @property
    def objects(self):
        terminator_objects = Terminators.pt_connection.get_frame_objects(self.ids)
        for terminator in terminator_objects:
            terminator = Terminators.set_terminator(terminator)
            logging.info('Working on terminator: {}'.format(terminator["id"]))
            ecocyc_terminator = Terminator(**terminator)
            yield ecocyc_terminator

    @staticmethod
    def set_terminator(terminator):
        new_terminator = dict(
            id=terminator[EC.ID],
            citations=terminator[EC.CITATIONS],
            comment=terminator[EC.COMMENT],
            dblinks=terminator[EC.DBLINKS],
            internal_comment=terminator[EC.INTERNAL_COMMENT],
            lend=terminator[EC.LEND],
            offset=10,
            organism=EC.ORGANISM_ID,
            rend=terminator[EC.REND]
        )
        return new_terminator
