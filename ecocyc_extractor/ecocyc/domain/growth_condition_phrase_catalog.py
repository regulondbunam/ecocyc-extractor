from .base import Base
from ..utils import constants as EC
from ..utils import utils


class GrowthConditionPhraseCatalog(Base):

    def __init__(self, **kwargs):
        super(GrowthConditionPhraseCatalog, self).__init__(**kwargs)
        self.description = kwargs.get("description", None)
        self.name = kwargs.get("name", None)
        self.terms = kwargs.get("terms", None)
