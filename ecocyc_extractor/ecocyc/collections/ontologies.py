"""
Ontologies collection
"""
# standard
import logging

# third party

# local
from ..utils.pathway_tools.connection import Connection
from ..utils import constants as EC
from ..domain.ontology import Ontology
from ..utils.utils import print_progress


class Ontologies(object, ):

    pt_connection = Connection()

    def __init__(self, ontology_name="gene-ontology"):
        self.ids = Ontologies.get_ids(ontology_name)

    @staticmethod
    def get_ids(ontology_name):
        if ontology_name == "gene-ontology":
            ontology_ids = [EC.GO_TERMS_CLASS]
        elif ontology_name == "multifun":
            ontology_ids = [EC.MULTIFUN_CLASS]
        else:
            ontology_ids = []
        return ontology_ids

    @property
    def objects(self):
        ontology_objects = Ontologies.pt_connection.get_frame_objects(self.ids)
        total_objects = len(list(ontology_objects))
        processed = 0
        for ontology in ontology_objects:
            ontology = Ontologies.set_ontology(ontology)
            logging.info("Working on ontology: {}".format(ontology["id"]))
            ecocyc_ontology = Ontology(**ontology)
            processed += 1
            print_progress(
                current=processed,
                total=total_objects,
                collection_name="Ontologies"
            )
            yield ecocyc_ontology

    @staticmethod
    def set_ontology(ontology):
        new_ontology = dict(
            id=ontology[EC.ID],
            dblinks=ontology[EC.DBLINKS],
            comment=ontology[EC.COMMENT],
        )
        return new_ontology
