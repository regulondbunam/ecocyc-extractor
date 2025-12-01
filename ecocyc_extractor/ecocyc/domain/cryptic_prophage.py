"""
cryptic_prophage extraction
"""
# standard

# third party

# local
from .base import Base


class CrypticProphage(Base):
    def __init__(self, **kwargs):
        super(CrypticProphage, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
