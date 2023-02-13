from .base import Base
from ..utils import constants as EC
from ..utils import utils


class Evidence(Base):
    def __init__(self, **kwargs):
        super(Evidence, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.code = kwargs.get("code", None)
        self.pertains_to = kwargs.get("pertains_to", None)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, name=None):
        if name is not None:
            self._code = (self.id).replace("EV-", "")
        else:
            self._code = None

    @property
    def pertains_to(self):
        return self._pertains_to

    @pertains_to.setter
    def pertains_to(self, classes=None):
        if classes is not None:
            pertains_to = []
            for class_id in classes:
                pertains_to.append(class_id.replace("|", ""))
            self._pertains_to = pertains_to
        else:
            self._pertains_to = None
