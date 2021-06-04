from .base import Base
from ..utils import constants as EC
from ..utils import utils


class Terminator(Base):
    def __init__(self, **kwargs):
        super(Terminator, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.class_ = kwargs.get("class", None)
        self.transcription_termination_site = kwargs.get("transcription_termination_site", None)

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
    def class_(self):
        return self._class

    @class_.setter
    def class_(self, class_):
        if class_ is None:
            terminator_class = self.pt_connection.get_instance_direct_types(self.id)
            if EC.RHO_INDEPENDENT in terminator_class:
                terminator_class = "rho-independent"
            elif EC.RHO_DEPENDENT in terminator_class:
                terminator_class = "rho-dependent"
            else:
                terminator_class = None
            self._class = terminator_class
        else:
            self._class = class_

    @property
    def transcription_termination_site(self):
        return self._transcription_termination_site

    @transcription_termination_site.setter
    def transcription_termination_site(self, transcription_termination_site=None):
        if transcription_termination_site is None:
            try:
                transcription_termination_site = {
                    "leftEndPosition": self.left_end_position,
                    "rightEndPosition": self.right_end_position,
                }
                # This will drop any key whose value is None
                transcription_termination_site = {k: v for k, v in transcription_termination_site.items() if v is not None}
            except TypeError:
                transcription_termination_site = None

        self._transcription_termination_site = transcription_termination_site
