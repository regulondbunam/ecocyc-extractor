"""
Growth Condition Phrase Catalog object
"""
# standard

# third party

# local
from .base import Base


class GrowthConditionPhraseCatalog(Base):

    def __init__(self, **kwargs):
        super(GrowthConditionPhraseCatalog, self).__init__(**kwargs)
        self.description = kwargs.get("description", None)
        self.name = kwargs.get("name", None)
        self.terms = kwargs.get("terms", None)
