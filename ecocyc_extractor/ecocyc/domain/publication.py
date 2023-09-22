from Bio import Entrez, Medline

from .base import Base
from ..utils import constants as EC
from ..utils import utils


class Publication(Base):
    def __init__(self, **kwargs):
        super(Publication, self).__init__(**kwargs)
        self.pmid = [kwargs.get("medline_id", None),
                     kwargs.get("pubmed_id", None)]
        self.authors = kwargs.get("authors", None)
        self.db_links = kwargs.get("dblinks", None)
        self.source = kwargs.get("source", None)
        self.title = kwargs.get("title", None)
        self.url = kwargs.get("url", None)
        self.year = kwargs.get("year", None)

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, authors=None):
        if authors:
            authors = authors
            if len(authors) != len(list(set(authors))):
                print(self.pmid)
                print(authors)
                print(list(set(authors)))
        self._authors = authors

    @property
    def pmid(self):
        return self._pmid

    @pmid.setter
    def pmid(self, references_ids):
        medline_id = references_ids[0]
        pubmed_id = references_ids[1]
        if pubmed_id is not None:
            self._pmid = pubmed_id
        elif medline_id is not None:
            self._pmid = medline_id
        else:
            self._pmid = None
