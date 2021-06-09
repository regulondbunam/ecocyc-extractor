from .base import Base
from ..utils import utils
from ..utils import constants as EC


class CrypticProphage(Base):
    def __init__(self, **kwargs):
        super(CrypticProphage, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
