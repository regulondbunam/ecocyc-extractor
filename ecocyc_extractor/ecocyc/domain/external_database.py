from .base import Base


class ExternalDatabase(Base):

    def __init__(self, **kwargs):
        super(ExternalDatabase, self).__init__(**kwargs)
        self.name = kwargs.get("id", None)
        self.description = kwargs.get("description", None)
        self.url = kwargs.get("url", None)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name.replace("|", "")