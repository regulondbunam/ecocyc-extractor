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