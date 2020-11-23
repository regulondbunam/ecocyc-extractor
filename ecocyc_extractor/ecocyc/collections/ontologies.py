import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC
from ecocyc_extractor.ecocyc.domain.ontology import Ontology


class Ontologies(object):

    pt_connection = Connection()

    def __init__(self):
        self.ids = Ontologies.get_ids()

    @staticmethod
    def get_ids():
        ontology_ids = [EC.GO_TERMS_CLASS, EC.MULTIFUN_CLASS]
        return ontology_ids

    @property
    def objects(self):
        ontology_objects = Ontologies.pt_connection.get_frame_objects(self.ids)
        for ontology in ontology_objects:
            ontology = Ontologies.set_ontology(ontology)
            logging.info('Working on ontology: {}'.format(ontology["id"]))
            ecocyc_ontology = Ontology(**ontology)
            yield ecocyc_ontology

    @staticmethod
    def set_ontology(ontology):
        new_ontology = dict(
            id=ontology[EC.ID],
            comment=ontology[EC.COMMENT]
        )
        return new_ontology