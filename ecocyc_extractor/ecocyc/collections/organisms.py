"""
Organisms collection
"""
# standard
import logging

# third party

# local
from ..utils.pathway_tools.connection import Connection
from ..domain.organism import Organism
from ..utils import constants as EC
from ..utils.utils import print_progress


class Organisms(object, ):

    pt_connection = Connection()

    def __init__(self, organism_name):
        self.ids = Organisms.get_ids(organism_name)

    @staticmethod
    def get_ids(organism_name):
        organism_ids = [organism_name]
        return organism_ids

    @property
    def objects(self):
        organism_objects = Organisms.pt_connection.get_frame_objects(self.ids)
        total_objects = len(list(organism_objects))
        processed = 0
        for organism in organism_objects:
            organism = Organisms.set_organism(organism)
            logging.info("Working on organism: {}".format(organism["id"]))
            ecocyc_organism = Organism(**organism)
            processed += 1
            print_progress(
                current=processed,
                total=total_objects,
                collection_name="Organisms"
            )
            yield ecocyc_organism

    @staticmethod
    def set_organism(organism):
        new_organism = dict(
            id=organism[EC.ID],
            db_links=organism[EC.DBLINKS],
            comment=organism[EC.COMMENT],
            citations=organism[EC.CITATIONS],
            genome=organism[EC.GENOME],
            comment_internal=organism[EC.INTERNAL_COMMENT],
            name=organism[EC.NAME],
            pgdb_authors=organism[EC.PGDB_AUTHORS],
            pgdb_copyright=organism[EC.PGDB_COPYRIGHT],
            pgdb_name=organism[EC.PGDB_NAME],
            strain_name=organism[EC.STRAIN_NAME],
            synonyms=organism[EC.SYNONYMS],
            url=organism[EC.PGDB_URL],
        )
        return new_organism
