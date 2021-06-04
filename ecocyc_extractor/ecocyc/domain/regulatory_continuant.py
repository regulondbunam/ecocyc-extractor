from .base import Base
from ..utils import constants as EC
from ..utils import utils
from ecocyc_extractor.ecocyc.collections.regulatory_interactions import (RegulatoryInteractions)


class RegulatoryContinuant(Base):

    regulatory_interaction_ids = RegulatoryInteractions.get_ids()

    def __init__(self, **kwargs):
        super(RegulatoryContinuant, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.type_ = kwargs.get("type", None)
        self.is_regulator = kwargs.get("regulates", None)

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
    def is_regulator(self):
        return self._is_regulator

    @is_regulator.setter
    def is_regulator(self, regulates=None):
        if regulates:
            for id_regulated in regulates:
                if id_regulated in RegulatoryContinuant.regulatory_interaction_ids:
                    regulates = True
                    break
                else:
                    regulates = False
        else:
            regulates = False
        self._is_regulator = regulates

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, _type=None):
        if _type is None:
            parent_class = self.pt_connection.get_frame_all_parents(self.id)
            if EC.COMPOUNDS_CLASS in parent_class:
                _type = "metabolite"
        self._type = _type