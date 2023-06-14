from .base import Base
from ..utils import constants as EC
from ..utils import utils
from ..collections.products import Products


class RegulatoryInteraction(Base):

    product_ids = Products.get_ids()
    compound_ids = Base.pt_connection.get_class_all_instances(
        EC.COMPOUNDS_CLASS)

    def __init__(self, **kwargs):
        super(RegulatoryInteraction, self).__init__(**kwargs)
        self.binding_site = kwargs.get("site", None)
        self.accessory_proteins = kwargs.get("accessory_proteins", None)
        self.db_links = kwargs.get("db_links", None)
        self.function_ = kwargs.get("mode", None)
        self.regulated_entity = kwargs.get("regulated_entity", None)
        self.regulated_entities = kwargs.get("regulated_entity", None)
        self.regulator = kwargs.get("regulator", None)
        self.mechanism = kwargs.get("mechanism", None)
        self.regulation_type = kwargs.get("regulation_type", None)
        self.relative_dist_site_promoter = kwargs.get(
            "relative_dist_site_promoter", None)
        self.regulation_class = kwargs.get("regulation_class", None)

    @property
    def regulation_type(self):
        return self._regulation_type

    @regulation_type.setter
    def regulation_type(self, regulation_type):
        # TODO: Cambiar propiedades
        all_parents = self.pt_connection.get_frame_all_parents(self.id)
        if EC.RNA_MEDIATED_TRANSLATION_REGULATION in all_parents:
            self._regulation_type = "sRNA-Regulation"
        elif EC.PROTEIN_MEDIATED_TRANSLATION_REGULATION in all_parents:
            self._regulation_type = "Protein-Regulation"
        elif EC.REGULATION_OF_TRANSCRIPTION in all_parents:
            self._regulation_type = "Transcription"
        else:
            self._regulation_type = "Unknown"

    @property
    def binding_site(self):
        return self._binding_site

    @binding_site.setter
    def binding_site(self, site_id=None):
        if isinstance(site_id, list):
            site_id = site_id[0]
        self._binding_site = site_id

    @property
    def relative_dist_site_promoter(self):
        return self._relative_dist_site_promoter

    @relative_dist_site_promoter.setter
    def relative_dist_site_promoter(self, relative_dist_site_promoter=None):
        if self.binding_site and self.regulated_entity:
            relative_dist_site_promoter = self.pt_connection.get_binding_site_promoter_offset(
                self.binding_site, self.regulated_entity["_id"])
        self._relative_dist_site_promoter = relative_dist_site_promoter

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
    def regulated_entity(self):
        return self._regulated_entity

    @regulated_entity.setter
    def regulated_entity(self, regulated_entity=None):
        if regulated_entity is not None:
            regulated_type = None
            regulated_entity_class = self.pt_connection.get_frame_all_parents(
                regulated_entity)

            if EC.TRANSCRIPTION_UNIT_CLASS in regulated_entity_class:
                regulated_type = "transcriptionUnit"
            elif EC.PROMOTER_CLASS in regulated_entity_class:
                regulated_type = "promoter"
            elif EC.GENE_CLASS in regulated_entity_class:
                regulated_type = "gene"

            self._regulated_entity = {
                "_id": regulated_entity,
                "name": self.pt_connection.get_name_by_id(regulated_entity),
                "type": regulated_type,
            }
            self._regulated_entity = self.get_only_properties_with_values(
                self._regulated_entity)
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
                "name": self.pt_connection.get_name_by_id(regulated_entity_id),
            }
            regulated_entity = self.get_only_properties_with_values(
                regulated_entity)

            regulated_entity_class = self.pt_connection.get_frame_direct_parents(
                regulated_entity_id)
            if EC.TRANSCRIPTION_UNIT_CLASS in regulated_entity_class:
                regulated_entity["type"] = "transcriptionUnit"
                regulated_entities.append(regulated_entity)
            elif EC.PROMOTER_CLASS in regulated_entity_class:
                regulated_entity["type"] = "promoter"

                sigma_factor_ids = self.pt_connection.get_promoter_sigma_factor(
                    regulated_entity_id)
                sigma_factor_ids = list(set(sigma_factor_ids))
                if len(sigma_factor_ids) > 1:
                    for sigma_factor_id in sigma_factor_ids:
                        regulated_entity["_id"] = ";".join(
                            [regulated_entity_id, sigma_factor_id])
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
                "type": regulator_type,
            }
            self._regulator = self.get_only_properties_with_values(
                self._regulator)
        else:
            self._regulator = regulator

    @property
    def regulation_class(self):
        return self._regulation_class

    @regulation_class.setter
    def regulation_class(self, regulation_class=None):
        if regulation_class is None:
            direct_parents = self.pt_connection.get_frame_direct_parents(
                self.id)
            self._regulation_class = direct_parents
        else:
            self._regulation_class = regulation_class
