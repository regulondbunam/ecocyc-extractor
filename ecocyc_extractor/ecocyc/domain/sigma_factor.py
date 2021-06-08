from .base import Base
from ..utils import constants as EC
from ..utils import utils


class SigmaFactor(Base):
    def __init__(self, **kwargs):
        super(SigmaFactor, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.gene = kwargs.get("gene", None)

    @property
    def gene(self):
        return self._gene

    @gene.setter
    def gene(self, gene=None):
        if isinstance(gene, list):
            self._gene = gene[0]
        else:
            self._gene = gene
