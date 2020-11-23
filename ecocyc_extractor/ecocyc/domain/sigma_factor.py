from .base import Base


class SigmaFactor(Base):

    def __init__(self, **kwargs):
        super(SigmaFactor, self).__init__(**kwargs)
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

