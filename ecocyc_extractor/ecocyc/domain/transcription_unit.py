from .base import Base
from ecocyc_extractor.ecocyc.collections.terminators import Terminators
from ..utils import constants as EC
from ..utils import utils


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
    def db_links(self):
        return self._db_links

    @db_links.setter
    def db_links(self, db_links):
        self._db_links = []
        try:
            self._db_links.extend(
                utils.get_external_cross_references(db_links))
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
    def gene_ids(self):
        return self._gene_ids

    @gene_ids.setter
    def gene_ids(self, gene_ids=None):
        if gene_ids is None:
            gene_ids = self.pt_connection.transcription_unit_genes(self.id)
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
                promoter_ids = [promoter_id]
        # TODO: promoters_id to string
        self._promoter_ids = promoter_ids

    @property
    def terminator_ids(self):
        return self._terminator_ids

    @terminator_ids.setter
    def terminator_ids(self, terminator_ids=None):
        if terminator_ids is None:
            self._terminator_ids = []
            tu_terminator_ids = self.pt_connection.transcription_unit_terminators(
                self.id
            )
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
