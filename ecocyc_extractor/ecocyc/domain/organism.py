"""
Organism object
"""
# standard

# third party

# local
from .base import Base
from ..utils import utils


class Organism(Base):
    # Connection to the database or management system, similar to the one used in Operon
    pt_connection = Base.pt_connection

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        # self.citations = kwargs.get("citations", None)
        # self.db_links = kwargs.get("db_links", None)
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
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name is None:
            name = self.id.replace("|", "")
        self._name = name

    @property
    def genome(self):
        return self._genome

    @genome.setter
    def genome(self, genome):
        genome = genome
        if genome is not None:
            genome = genome[0]
            genome_name = Organism.pt_connection.get_slot_value(genome, "|COMMON-NAME|")
            genome_name = None
            if genome_name is None:
                self._genome = genome_name
        self._genome = genome

    @property
    def synonyms(self):
        return self._synonyms

    @synonyms.setter
    def synonyms(self, synonyms=None):
        gene_id = self.id.replace("|", "")
        self._synonyms = synonyms
        try:
            self._synonyms.append(gene_id)
        except AttributeError:
            self._synonyms = [gene_id]

    @staticmethod
    def get_only_properties_with_values(properties):
        properties = {k: v for k, v in properties.items() if v is not None}
        return properties

