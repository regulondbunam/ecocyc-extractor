from .base import Base
from ..utils import constants as EC
from ..utils import utils
from ..collections.products import Products
from ..collections.transcription_factors import TranscriptionFactors


class RegulatoryComplex(Base):

    product_ids = Products.get_ids()
    compound_ids = Base.pt_connection.get_class_all_instances(EC.COMPOUNDS_CLASS)
    compound_ids.extend(Base.pt_connection.get_class_all_subs(EC.COMPOUNDS_CLASS))
    transcription_factor_ids = TranscriptionFactors.get_ids()

    def __init__(self, **kwargs):
        super(RegulatoryComplex, self).__init__(**kwargs)
        self.abbreviated_name = kwargs.get("abbreviated_name", None)
        self.compounds = kwargs.get("compounds", None)
        self._components = kwargs.get("components", None)
        self.db_links = kwargs.get("db_links", None)
        self._unmodified_form = kwargs.get("unmodified_form", None)
        self.products = kwargs.get("products", None)
        self._regulates = kwargs.get("regulates", None)
        self.type_ = kwargs.get("type", None)
        self.is_transcription_factor = kwargs.get("is_transcription_factor", None)

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
    def compounds(self):
        return self._compounds

    @compounds.setter
    def compounds(self, compounds=None):
        if compounds:
            self._compounds = compounds
        else:
            self._compounds = None

    @property
    def is_transcription_factor(self):
        return self._is_transcription_factor

    @is_transcription_factor.setter
    def is_transcription_factor(self, is_transcription_factor=None):
        if is_transcription_factor is None:
            is_transcription_factor = (
                True if self.id in RegulatoryComplex.transcription_factor_ids else False
            )
        self._is_transcription_factor = is_transcription_factor

    @property
    def products(self):
        return self._products

    @products.setter
    def products(self, products=None):
        if products is None:
            if self._components is not None:
                products, compounds = RegulatoryComplex.get_components(
                    self.id, self._components
                )
                self.compounds = list(compounds)
            elif self._components is None and self._unmodified_form is not None:
                products, compounds = self.get_unmodified_form_products(
                    self._unmodified_form
                )
                self.compounds = list(compounds)
        self._products = products

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, _type=None):
        if _type is None:
            if self._regulates:
                _type = "active"
            else:
                _type = "inactive"
        self._type = _type

    @staticmethod
    def get_unmodified_form_products(unmodified_form_id):
        products = []
        compounds = []
        if unmodified_form_id in RegulatoryComplex.product_ids:
            products = [{"products_id": unmodified_form_id}]
        else:
            component_ids = RegulatoryComplex.pt_connection.get_slot_values(
                unmodified_form_id, EC.SLOT_COMPONENTS_CLASS
            )
            for component_id in component_ids:
                if component_id in RegulatoryComplex.product_ids:
                    coefficient = RegulatoryComplex.pt_connection.get_value_annot(
                        unmodified_form_id,
                        EC.SLOT_COMPONENTS_CLASS,
                        component_id,
                        EC.SLOT_COEFFICIENT_CLASS,
                    )
                    product_object = {
                        "products_id": component_id,
                        "coefficient": coefficient,
                    }
                    product_object = RegulatoryComplex.get_only_properties_with_values(
                        product_object
                    )
                    if product_object not in products:
                        products.append(product_object.copy())
                else:
                    coefficient = RegulatoryComplex.pt_connection.get_value_annot(
                        unmodified_form_id,
                        EC.SLOT_COMPONENTS_CLASS,
                        component_id,
                        EC.SLOT_COEFFICIENT_CLASS,
                    )
                    sub_components = RegulatoryComplex.pt_connection.get_slot_values(
                        component_id, EC.SLOT_COMPONENTS_CLASS
                    )
                    for sub_component in sub_components:
                        if (
                            sub_component not in RegulatoryComplex.product_ids
                            and sub_component not in RegulatoryComplex.compound_ids
                        ):
                            raise ValueError(
                                "Could not find a product or compound id for the object {}".format(
                                    sub_component
                                )
                            )
                        elif sub_component in RegulatoryComplex.product_ids:
                            sub_coefficient = (
                                RegulatoryComplex.pt_connection.get_value_annot(
                                    component_id,
                                    EC.SLOT_COMPONENTS_CLASS,
                                    sub_component,
                                    EC.SLOT_COEFFICIENT_CLASS,
                                )
                            )
                            if coefficient is not None and sub_coefficient is not None:
                                coefficient *= sub_coefficient
                            elif coefficient is None and sub_coefficient is not None:
                                coefficient = sub_coefficient
                            product_object = {
                                "product_id": sub_component,
                                "coefficient": coefficient,
                            }
                            product_object = {
                                k: v for k, v in product_object.items() if v is not None
                            }
                            products.append(product_object.copy())
                        elif (
                            sub_component in RegulatoryComplex.compound_ids
                            and sub_component not in compounds
                        ):
                            compounds.append(sub_component)
        return products, compounds

    @staticmethod
    def get_components(protein_id, components):
        products = []
        compounds = []
        for component in components:
            if (
                component not in RegulatoryComplex.product_ids
                and component not in RegulatoryComplex.compound_ids
            ):
                unmodified_form = RegulatoryComplex.pt_connection.get_slot_value(
                    component, EC.SLOT_UNMODIFIED_FORM_CLASS
                )
                if unmodified_form in RegulatoryComplex.product_ids:
                    product_object = {"products_id": unmodified_form}
                    products.append(product_object.copy())
                else:
                    coefficient = RegulatoryComplex.pt_connection.get_value_annot(
                        protein_id,
                        EC.SLOT_COMPONENTS_CLASS,
                        component,
                        EC.SLOT_COEFFICIENT_CLASS,
                    )
                    sub_components = RegulatoryComplex.pt_connection.get_slot_values(
                        component, EC.SLOT_COMPONENTS_CLASS
                    )
                    for sub_component in sub_components:
                        sub_coefficient = (
                            RegulatoryComplex.pt_connection.get_value_annot(
                                component,
                                EC.SLOT_COMPONENTS_CLASS,
                                sub_component,
                                EC.SLOT_COEFFICIENT_CLASS,
                            )
                        )
                        if (
                            sub_component not in RegulatoryComplex.product_ids
                            and sub_component not in RegulatoryComplex.compound_ids
                        ):
                            unmodified_form_sub_component = (
                                RegulatoryComplex.pt_connection.get_slot_value(
                                    sub_component, EC.SLOT_UNMODIFIED_FORM_CLASS
                                )
                            )
                            if (
                                unmodified_form_sub_component
                                in RegulatoryComplex.product_ids
                            ):
                                product_object = {
                                    "products_id": unmodified_form_sub_component,
                                    "coefficient": coefficient,
                                }
                                product_object = {
                                    k: v
                                    for k, v in product_object.items()
                                    if v is not None
                                }
                                products.append(product_object.copy())
                            else:
                                sub_sub_components = (
                                    RegulatoryComplex.pt_connection.get_slot_values(
                                        sub_component, EC.SLOT_COMPONENTS_CLASS
                                    )
                                )
                                for sub_sub_component in sub_sub_components:
                                    sub_sub_coefficient = (
                                        RegulatoryComplex.pt_connection.get_value_annot(
                                            sub_component,
                                            EC.SLOT_COMPONENTS_CLASS,
                                            sub_sub_component,
                                            EC.SLOT_COEFFICIENT_CLASS,
                                        )
                                    )
                                    coefficient_1 = coefficient if coefficient else 1
                                    sub_coefficient_1 = (
                                        sub_coefficient if sub_coefficient else 1
                                    )
                                    if sub_sub_coefficient:
                                        sub_sub_coefficient *= (
                                            coefficient_1 * sub_coefficient_1
                                        )
                                    if (
                                        sub_sub_component
                                        in RegulatoryComplex.product_ids
                                    ):
                                        product_object = {
                                            "products_id": sub_sub_component,
                                            "coefficient": sub_sub_coefficient,
                                        }
                                        product_object = {
                                            k: v
                                            for k, v in product_object.items()
                                            if v is not None
                                        }
                                        products.append(product_object.copy())
                                    elif (
                                        sub_sub_component
                                        in RegulatoryComplex.compound_ids
                                        and sub_sub_component not in compounds
                                    ):
                                        compounds.append(sub_component)
                                    else:
                                        raise ValueError(
                                            "Could not find a product id for the protein {}-->{}".format(
                                                protein_id, sub_sub_component
                                            )
                                        )
                        elif sub_component in RegulatoryComplex.product_ids:
                            if coefficient is not None and sub_coefficient is not None:
                                sub_coefficient *= coefficient
                            elif coefficient is None and sub_coefficient is not None:
                                sub_coefficient = coefficient
                            product_object = {
                                "products_id": sub_component,
                                "coefficient": sub_coefficient,
                            }
                            product_object = {
                                k: v for k, v in product_object.items() if v is not None
                            }
                            products.append(product_object.copy())
                        elif (
                            sub_component in RegulatoryComplex.compound_ids
                            and sub_component not in compounds
                        ):
                            compounds.append(sub_component)
            elif component in RegulatoryComplex.product_ids:
                coefficient = RegulatoryComplex.pt_connection.get_value_annot(
                    protein_id,
                    EC.SLOT_COMPONENTS_CLASS,
                    component,
                    EC.SLOT_COEFFICIENT_CLASS,
                )
                product_id = component
                product_object = {"products_id": product_id, "coefficient": coefficient}
                product_object = {
                    k: v for k, v in product_object.items() if v is not None
                }
                products.append(product_object.copy())
            elif (
                component in RegulatoryComplex.compound_ids
                and component not in compounds
            ):
                compounds.append(component)
        return products, compounds
