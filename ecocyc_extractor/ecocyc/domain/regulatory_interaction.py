from .base import Base
from ..utils import constants as EC
from ..collections.products import Products


class RegulatoryInteraction(Base):

    product_ids = Products.get_ids()
    compound_ids = Base.pt_connection.get_class_all_instances(EC.COMPOUNDS_CLASS)

    def __init__(self, **kwargs):
        super(RegulatoryInteraction, self).__init__(**kwargs)
        self.binding_site = kwargs.get("site", None)
        self.function_ = kwargs.get("mode", None)
        self.regulated_entity = kwargs.get("regulated_entity", None)
        self.regulated_entities = kwargs.get("regulated_entity", None)
        self.regulator = kwargs.get("regulator", None)
        self.center_position = kwargs.get("center_position", None)
        self.gene = kwargs.get("gene", None)
        self.promoters = kwargs.get("promoter", None)

    @property
    def binding_site(self):
        return self._binding_site

    @binding_site.setter
    def binding_site(self, site_id=None):
        if isinstance(site_id, list):
            site_id = site_id[0]
        self._binding_site = RegulatoryInteraction.get_site(site_id)

    @property
    def center_position(self):
        return self._center_position

    @center_position.setter
    def center_position(self, center_position=None):
        if self.binding_site and self.regulated_entity:
            center_position = self.pt_connection.get_binding_site_promoter_offset(self.binding_site["_id"], self.regulated_entity["_id"])
        self._center_position = center_position

    @property
    def function_(self):
        return self._function

    @function_.setter
    def function_(self, _function=None):
        if _function is not None:
            if "+" in _function:
                _function = "activator"
            elif "-" in _function:
                _function = "repressor"
        self._function = _function

    @property
    def gene(self):
        return self._gene

    @gene.setter
    def gene(self, gene=None):
        if gene is None and self.regulated_entity is not None:

            if self.regulated_entity["type"] == "promoter":
                transcription_unit_ids = self.pt_connection.transcription_units_of_promoter(self.regulated_entity["_id"])
            else:
                transcription_unit_ids = [self.regulated_entity["_id"]]
            
            tus_first_gene = []
            if self.binding_site:
                tu_strand = 1
                for transcription_unit_id in transcription_unit_ids:
                    tu_strand = self.pt_connection.get_transcription_direction(transcription_unit_id)
                    gene_id = self.pt_connection.get_tu_first_gene(transcription_unit_id)
                    site_relative_gene_pos = self.pt_connection.site_pos_relative_to_first_gene(self.binding_site["_id"], transcription_unit_id)
                    tus_first_gene.append((gene_id, site_relative_gene_pos))
                try:
                    tus_first_gene = sorted(tus_first_gene, key=lambda relative_pos: relative_pos[1])
                    gene_id, distance = tus_first_gene[-1] if tu_strand == -1 else tus_first_gene[0]
                    gene_fragment = self.pt_connection.get_slot_value(gene_id, EC.FRAGMENT_OF_SLOT)
                    if gene_fragment:
                        gene_id = gene_fragment
                    gene = {
                        "gene_id": gene_id,
                        "gene_name": self.pt_connection.get_name_by_id(gene_id),
                        "distanceTo": distance
                    }
                    gene = self.get_only_properties_with_values(gene)
                except IndexError:
                    gene = None
        self._gene = gene

    @property
    def promoters(self):
        return self._promoters

    @promoters.setter
    def promoters(self, promoters=None):
        if promoters is None:
            if self.regulated_entity:
                if self.regulated_entity["type"] == "promoter":
                    promoters = []
                    promoter_id = self.regulated_entity["_id"]
                    center_position = self.center_position
                    name = self.pt_connection.get_name_by_id(self.regulated_entity["_id"])
                    promoter = {
                        "promoter_id": promoter_id,
                        "distanceTo": center_position,
                        "promoter_name": name
                    }
                    promoter = self.get_only_properties_with_values(promoter)

                    sigma_factor_ids = self.pt_connection.get_promoter_sigma_factor(promoter_id)
                    sigma_factor_ids = list(set(sigma_factor_ids))
                    if len(sigma_factor_ids) > 1:
                        for sigma_factor_id in sigma_factor_ids:
                            promoter["promoter_id"] = ";".join([promoter_id, sigma_factor_id])
                            promoters.append(promoter.copy())
                    else:
                        promoters.append(promoter.copy())

        self._promoters = promoters

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
    def regulated_entities(self):
        return self._regulated_entities

    @regulated_entities.setter
    def regulated_entities(self, regulated_entity_id=None):
        if regulated_entity_id is not None:

            regulated_entities = []
            regulated_entity = {
                "_id": regulated_entity_id,
                "name": self.pt_connection.get_name_by_id(regulated_entity_id)
            }
            regulated_entity = self.get_only_properties_with_values(regulated_entity)

            regulated_entity_class = self.pt_connection.get_frame_direct_parents(regulated_entity_id)
            if EC.TRANSCRIPTION_UNIT_CLASS in regulated_entity_class:
                regulated_entity["type"] = "transcriptionUnit"
                regulated_entities.append(regulated_entity)
            elif EC.PROMOTER_CLASS in regulated_entity_class:
                regulated_entity["type"] = "promoter"

                sigma_factor_ids = self.pt_connection.get_promoter_sigma_factor(regulated_entity_id)
                sigma_factor_ids = list(set(sigma_factor_ids))
                if len(sigma_factor_ids) > 1:
                    for sigma_factor_id in sigma_factor_ids:
                        regulated_entity["_id"] = ";".join([regulated_entity_id, sigma_factor_id])
                        regulated_entities.append(regulated_entity.copy())
                else:
                    regulated_entities.append(regulated_entity.copy())
            self._regulated_entities = regulated_entities
        else:
            self._regulated_entities = None

    @property
    def regulator(self):
        return self._regulator

    @regulator.setter
    def regulator(self, regulator=None):
        if regulator is not None:
            if regulator in self.product_ids:
                regulator_type = "product"
            elif regulator in self.compound_ids:
                regulator_type = "regulatoryContinuant"
            else:
                regulator_type = "regulatoryComplex"

            self._regulator = {
                "_id": regulator,
                "name": self.pt_connection.get_name_by_id(regulator),
                "type": regulator_type
            }
            self._regulator = self.get_only_properties_with_values(self._regulator)
        else:
            self._regulator = regulator

    @staticmethod
    def get_site(site_id=None):
        if site_id is not None:
            site = RegulatoryInteraction.pt_connection.get_frame_objects([site_id])[0]
            site = RegulatoryInteraction.set_site(site)
            site = Site(site)
            site_object = site.to_dict()
        else:
            site_object = None
        return site_object

    @staticmethod
    def set_site(site):
        new_site = dict(
            id=site[EC.ID],
            absolute_position=site[EC.ABSOLUTE_CENTER_POSITION],
            citations=site[EC.CITATIONS],
            comment=site[EC.COMMENT],
            dblinks=site[EC.DBLINKS],
            internal_comment=site[EC.INTERNAL_COMMENT],
            length=site[EC.DNA_FOOTPRINT_SIZE],
        )
        return new_site


class Site(Base):
    def __init__(self, kwargs):
        super(Site, self).__init__(**kwargs)
        self.absolute_position = kwargs.get("absolute_position", None)
        self.length = kwargs.get("length", None)
        self.left_end_position = kwargs.get("lend", None)
        self.right_end_position = kwargs.get("rend", None)
        self.sequence = kwargs.get("sequence", None)

    def to_dict(self):
        site = dict(
            _id=self.id,
            absolutePosition=self.absolute_position,
            citations=self.citations,
            externalCrossReferences=self.db_links,
            internalComment=self.internal_comment,
            leftEndPosition=self.left_end_position,
            length=self.length,
            note=self.comment,
            rightEndPosition=self.right_end_position,
            sequence=self.sequence
        )
        site = self.get_only_properties_with_values(site)
        return site

    @property
    def left_end_position(self):
        if self._left_end_position == self._right_end_position:
            self._left_end_position = None
            self._right_end_position = None
        return self._left_end_position

    @left_end_position.setter
    def left_end_position(self, lend=None):
        if lend is None:
            lend = self.pt_connection.get_site_left_position_extended(self.id)
        self._left_end_position = lend

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length=None):
        if length is None:
            length = self.pt_connection.binding_site_size(self.id)
        self._length = length

    @property
    def right_end_position(self):
        if self._left_end_position == self._right_end_position:
            self._right_end_position = None
            self._left_end_position = None
        return self._right_end_position

    @right_end_position.setter
    def right_end_position(self, rend=None):
        if rend is None:
            rend = self.pt_connection.get_site_right_position_extended(self.id)
        self._right_end_position = rend

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence=None, strand=None, offset=10):
        """

        :param sequence:
        :param strand:
        :param offset:
        :return:
        """
        if sequence is None and strand is not None:
            try:
                # if both positions have identical values then it means that there's an inconsistency
                # on the site positions' data or pathway tool's functions
                if self.left_end_position == self.right_end_position:
                    sequence = None
                else:
                    sequence = Base.get_sequence(self.left_end_position, self.right_end_position, strand, offset)
            except TypeError:
                self._sequence = None
        self._sequence = sequence
