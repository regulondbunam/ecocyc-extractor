from .base import Base
from ..utils import constants as EC
from ..utils import utils


class SigmaFactor(Base):
    def __init__(self, **kwargs):
        super(SigmaFactor, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.gene = kwargs.get("gene", None)

    @property
    def db_links(self):
        return self._db_links

    @db_links.setter
    def db_links(self, db_links):
        self._db_links = []
        try:
            self._db_links.extend(utils.get_external_cross_references(db_links))
        except TypeError:
            pass

        ecocyc_reference = {
            "externalCrossReferences_id": "|ECOCYC|",
            "objectId": self.id.replace("|", ""),
        }
        self._db_links.append(ecocyc_reference.copy())

        if self.bnumber:
            bnumber_reference = {
                "externalCrossReferences_id": "|REFSEQ|",
                "objectId": self.bnumber,
            }
            self._db_links.append(bnumber_reference.copy())

    @property
    def gene(self):
        return self._gene

    @gene.setter
    def gene(self, gene=None):
        if isinstance(gene, list):
            self._gene = gene[0]
        else:
            self._gene = gene
