import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC
from ecocyc_extractor.ecocyc.domain.term import Term


class Terms(object):
    MULTIFUN = "multifun"
    GENE_ONTOLOGY = "gene-ontology"

    pt_connection = Connection()

    def __init__(self, term_type=True):
        self.ids = Terms.get_ids(term_type)

    @staticmethod
    def get_ids(term_type):
        if term_type == Terms.MULTIFUN:
            term_ids = Terms.pt_connection.get_class_all_subs(EC.MULTIFUN_CLASS)
        elif term_type == Terms.GENE_ONTOLOGY:
            term_ids = Terms.pt_connection.get_class_all_subs(EC.GO_TERMS_CLASS)
        else:
            term_ids = []
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
