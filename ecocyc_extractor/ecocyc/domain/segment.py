from .base import Base
from ..utils import utils
from ..utils import constants as EC


class Segment(Base):
    def __init__(self, **kwargs):
        super(Segment, self).__init__(**kwargs)
        self.binding_site = kwargs.get("site", None)
        self.regulated_entity = kwargs.get("regulated_entity", None)
        self.db_links = kwargs.get("dblinks", None)
        self.parent = kwargs.get("parent", None)
        self.segment_type = kwargs.get("segment_type", None)
        self.center_position = kwargs.get("center_position", None)

    @property
    def binding_site(self):
        return self._binding_site

    @binding_site.setter
    def binding_site(self, site_id=None):
        if isinstance(site_id, list):
            site_id = site_id[0]
        self._binding_site = site_id

    @property
    def regulated_entity(self):
        return self._regulated_entity

    @regulated_entity.setter
    def regulated_entity(self, regulated_entity=None):
        if regulated_entity is not None:
            regulated_type = None
            regulated_entity_class = self.pt_connection.get_frame_direct_parents(regulated_entity)
            if EC.TRANSCRIPTION_UNIT_CLASS in regulated_entity_class:
                regulated_type = "transcriptionUnit"
            elif EC.PROMOTER_CLASS in regulated_entity_class:
                regulated_type = "promoter"

            self._regulated_entity = {
                "_id": regulated_entity,
                "name": self.pt_connection.get_name_by_id(regulated_entity),
                "type": regulated_type,
            }
            self._regulated_entity = self.get_only_properties_with_values(self._regulated_entity)
        else:
            self._regulated_entity = None

    @property
    def center_position(self):
        return self._center_position

    @center_position.setter
    def center_position(self, center_position=None):
        if self.binding_site and self.regulated_entity:
            center_position = self.pt_connection.get_binding_site_promoter_offset(self.binding_site, self.regulated_entity["_id"])
        self._center_position = center_position

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        all_parents = self.pt_connection.get_frame_all_parents(self.id)
        index_of = all_parents.index(EC.POLYMER_SEGMENTS)
        self._parent = all_parents[index_of + 2]

    @property
    def segment_type(self):
        return self._segment_type

    @segment_type.setter
    def segment_type(self, segment_type):
        all_parents = self.pt_connection.get_frame_all_parents(self.id)
        if EC.MRNA_SEGMENTS in all_parents:
            self._segment_type = EC.MRNA_SEGMENTS
        elif EC.DNA_SEGMENTS in all_parents:
            self._segment_type = EC.DNA_SEGMENTS
        else:
            self._segment_type = None
