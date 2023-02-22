from .base import Base
from ..utils import constants as EC
from ..utils import utils


class Ontology(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.db_links = kwargs.get("dblinks", None)
        self.comment = kwargs.get("comment", None)
        self.name = kwargs.get("name", None)

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment=None):
        if comment is not None:
            comment = Base.get_comment(comment)
        self._comment = comment

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if name is None:
            name = self.id
            name = name.replace("|", "").replace("-", " ")
        self._name = name
