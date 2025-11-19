"""
Organism object
"""
# standard

# third party

# local
from .base import Base
from ..utils import utils


class Organism(object):
    # Connection to the database or management system, similar to the one used in Operon
    pt_connection = Base.pt_connection

    def __init__(self, **kwargs):
        self.id = kwargs.get("_id", None)
        self.citations = kwargs.get("citations", None)
        self.db_links = kwargs.get("db_links", None)
        self.comment = kwargs.get("comment", None)
        self.genome = kwargs.get("genome", None)
        self.comment_internal = kwargs.get("comment_internal", None)
        self.name = kwargs.get("name", None)
        self.pgdb_authors = kwargs.get("pgdb_authors", None)
        self.pgdb_copyright = kwargs.get("pgdb_copyright", None)
        self.pgdb_name = kwargs.get("pgdb_name", None)
        self.strain_name = kwargs.get("strain_name", None)
        self.synonyms = kwargs.get("synonyms", None)
        self.url = kwargs.get("url", None)

    # --- Properties with Getters and Setters ---
    # TODO: Add DB_LINKS

    @staticmethod
    def get_only_properties_with_values(properties):
        properties = {k: v for k, v in properties.items() if v is not None}
        return properties