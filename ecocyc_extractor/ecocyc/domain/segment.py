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
            regulated_entity_class = self.pt_connection.get_frame_direct_parents(
                regulated_entity
            )
            if EC.TRANSCRIPTION_UNIT_CLASS in regulated_entity_class:
                regulated_type = "transcriptionUnit"
            elif EC.PROMOTER_CLASS in regulated_entity_class:
                regulated_type = "promoter"

            self._regulated_entity = {
                "_id": regulated_entity,
                "name": self.pt_connection.get_name_by_id(regulated_entity),
                "type": regulated_type,
            }
            self._regulated_entity = self.get_only_properties_with_values(
                self._regulated_entity
            )
        else:
            self._regulated_entity = None

    @property
    def center_position(self):
        return self._center_position

    @center_position.setter
    def center_position(self, center_position=None):
        if self.binding_site and self.regulated_entity:
            center_position = self.pt_connection.get_binding_site_promoter_offset(
                self.binding_site, self.regulated_entity["_id"]
            )
        self._center_position = center_position

    @property
    def db_links(self):
        return self._db_links

    @db_links.setter
    def db_links(self, db_links):
        self._db_links = []
        try:
            self._db_links.extend(
                utils.get_external_cross_references(db_links))
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
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        all_parents = self.pt_connection.get_frame_all_parents(self.id)
        if EC.GENES in all_parents:
            self._parent = EC.GENES
        elif EC.PHANTOM_GENES in all_parents:
            self._parent = EC.PHANTOM_GENES
        elif EC.PSEUDO_GENES in all_parents:
            self._parent = EC.PSEUDO_GENES
        elif EC.TRUNCATED_GENES in all_parents:
            self._parent = EC.TRUNCATED_GENES
        elif EC.CRYPTIC_PROPHAGES in all_parents:
            self._parent = EC.CRYPTIC_PROPHAGES
        elif EC.DNA_BINDING_SITES in all_parents:
            self._parent = EC.DNA_BINDING_SITES
        elif EC.EXTRAGENIC_SITES in all_parents:
            self._parent = EC.EXTRAGENIC_SITES
        elif EC.GENE_FRAGMENTS in all_parents:
            self._parent = EC.GENE_FRAGMENTS
        elif EC.GENOMIC_ISLANDS in all_parents:
            self._parent = EC.GENOMIC_ISLANDS
        elif EC.MISC_FEATURES in all_parents:
            self._parent = EC.MISC_FEATURES
        elif EC.PROMOTER_CLASS in all_parents:
            self._parent = EC.PROMOTER_CLASS
        elif EC.PROPHAGES in all_parents:
            self._parent = EC.PROPHAGES
        elif EC.REPLICON_BUCKETS in all_parents:
            self._parent = EC.REPLICON_BUCKETS
        elif EC.RECOMBINATION_SITES in all_parents:
            self._parent = EC.RECOMBINATION_SITES
        elif EC.SPNS in all_parents:
            self._parent = EC.SPNS
        elif EC.TRANSCRIPTION_UNIT_CLASS in all_parents:
            self._parent = EC.TRANSCRIPTION_UNIT_CLASS
        elif EC.MRNA_BINDING_SITES in all_parents:
            self._parent = EC.MRNA_BINDING_SITES
        elif EC.TERMINATOR_CLASS in all_parents:
            self._parent = EC.TERMINATOR_CLASS
        elif EC.TRANSPOSONS in all_parents:
            self._parent = EC.TRANSPOSONS
        else:
            self._parent = None
            print(self.id)

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
