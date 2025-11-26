"""
Transcription Unit object
"""
# standard

# third party

# local
from .base import Base
from ..collections.terminators import Terminators


class TranscriptionUnit(Base):

    _operon_ids = Base.pt_connection.all_operons()
    _all_terminator_class_ids = Terminators.get_ids()

    def __init__(self, **kwargs):
        super(TranscriptionUnit, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.gene_ids = kwargs.get("genes", None)
        self.promoter_ids = kwargs.get("promoter", None)
        self.operon_id = kwargs.get("operon", None)
        self.terminator_ids = kwargs.get("terminator", None)

    @property
    def gene_ids(self):
        return self._gene_ids

    @gene_ids.setter
    def gene_ids(self, gene_ids=None):
        pseudo_genes = [
            '|Gene-Fragments|',
        ]
        if gene_ids is None:
            cyc_gene_ids = self.pt_connection.transcription_unit_genes(self.id)
            gene_ids = []
            for gene_id in cyc_gene_ids:
                if self.pt_connection.get_frame_direct_parents(gene_id) not in pseudo_genes:
                    gene_ids.append(gene_id)
        self._gene_ids = gene_ids

    @property
    def promoter_ids(self):
        return self._promoter_ids

    @promoter_ids.setter
    def promoter_ids(self, promoter_id=None):
        promoter_ids = None
        if promoter_id is None:
            promoter_id = self.pt_connection.transcription_unit_promoter(
                self.id)
        if promoter_id:
            sigma_factor_ids = self.pt_connection.get_promoter_sigma_factor(
                promoter_id)
            sigma_factor_ids = list(set(sigma_factor_ids))
            if len(sigma_factor_ids) > 1:
                promoter_ids = []
                for sigma_factor_id in sigma_factor_ids:
                    promoter_ids.append(
                        ";".join([promoter_id, sigma_factor_id]))
            else:
                promoter_ids = promoter_id
        self._promoter_ids = promoter_ids

    @property
    def terminator_ids(self):
        return self._terminator_ids

    @terminator_ids.setter
    def terminator_ids(self, terminator_ids=None):
        if terminator_ids is None:
            self._terminator_ids = []
            tu_terminator_ids = self.pt_connection.transcription_unit_terminators(
                self.id)
            tu_terminator_ids = tu_terminator_ids
            for tu_terminator_id in tu_terminator_ids:
                if tu_terminator_id in self._all_terminator_class_ids:
                    self._terminator_ids.append(tu_terminator_id)
            if not self._terminator_ids:
                self._terminator_ids = None
        else:
            self._terminator_ids = terminator_ids

    @property
    def operon_id(self):
        return self._operon_id

    @operon_id.setter
    def operon_id(self, operon_id=None):
        if operon_id is None:
            for operon_tu_ids in self._operon_ids:
                if self.id in operon_tu_ids:
                    operon_id = ";".join(operon_tu_ids)
        self._operon_id = operon_id
