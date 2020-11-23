import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC
from ecocyc_extractor.ecocyc.domain.term import Term


class Terms(object):

    pt_connection = Connection()

    def __init__(self):
        self.ids = Terms.get_ids()

    @staticmethod
    def get_ids():
        multifun_ids = Terms.pt_connection.get_class_all_subs(EC.MULTIFUN_CLASS)
        go_term_ids = Terms.pt_connection.get_class_all_subs(EC.GO_TERMS_CLASS)
        term_ids = multifun_ids + go_term_ids
        return term_ids

    @property
    def objects(self):
        term_objects = Terms.pt_connection.get_frame_objects(self.ids)
        for term in term_objects:
            term = Terms.set_term(term)
            logging.info('Working on term: {}'.format(term["id"]))
            ecocyc_term = Term(**term)
            yield ecocyc_term

    @staticmethod
    def set_term(term):
        new_term = dict(
            id=term[EC.ID],
            comment=term[EC.COMMENT],
            definition=term[EC.DEFINITION],
            dblinks=term[EC.DBLINKS],
            name=term[EC.NAME],
            synonyms=term[EC.SYNONYMS],
            term_members=term[EC.TERM_MEMBERS]
        )
        return new_term
