from .base import Base
from ..utils import constants as EC
from ..utils import utils
from ..collections.products import Products


class TranscriptionFactor(Base):

    product_ids = Products.get_ids()

    def __init__(self, **kwargs):
        super(TranscriptionFactor, self).__init__(**kwargs)
        self.tf_ids = kwargs.get('tf_ids', None)
        self.db_links = kwargs.get("dblinks", None)
        self.abbreviated_name = kwargs.get("abbreviated_name", None)
        self.active_conformations = kwargs.get("active_conformations", None)
        self.citations = kwargs.get("citations", None)
        self.global_function = None
        self.inactive_conformations = kwargs.get(
            "inactive_conformations", None)
        self.name = kwargs.get("name", None)
        self.site_length = kwargs.get("site_length", None)
        self.symmetry = kwargs.get("symmetry", None)

    @property
    def active_conformations(self):
        return self._active_conformations

    @active_conformations.setter
    def active_conformations(self, active_conformations):
        if active_conformations is None:
            tf_active_conformations = []
            for conformation_id in TranscriptionFactor.get_tf_active_conformations(self.id):
                if conformation_id in self.tf_ids:
                    continue
                if conformation_id in TranscriptionFactor.product_ids:
                    conformation_class = "product"
                else:
                    conformation_class = "regulatoryComplex"
                tf_active_conformations.append(
                    {"_id": conformation_id, "type": conformation_class})
            self._active_conformations = tf_active_conformations
        else:
            self._active_conformations = active_conformations

    @property
    def inactive_conformations(self):
        return self._inactive_conformations

    @inactive_conformations.setter
    def inactive_conformations(self, inactive_conformations):
        if inactive_conformations is None:
            tf_inactive_conformations = []
            for conformation_id in TranscriptionFactor.get_tf_inactive_conformations(self.id):
                if conformation_id in self.tf_ids:
                    continue
                tf_inactive_conformations.append(
                    {"_id": conformation_id, "type": "regulatoryComplex"})
            self._inactive_conformations = tf_inactive_conformations
        else:
            self._inactive_conformations = inactive_conformations

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self.abbreviated_name is not None:
            self._name = self.abbreviated_name
        else:
            self._name = name

    @property
    def global_function(self):
        return self._global_function

    @global_function.setter
    def global_function(self, global_function=None):
        regulates = []
        if global_function is None:
            for conformation in self.active_conformations:
                regulates = self.pt_connection.get_slot_values(
                    conformation["_id"], EC.REGULATES_SLOT)
            global_function = TranscriptionFactor.get_protein_function(
                regulates)
        self._global_function = global_function

    @property
    def site_length(self):
        return self._site_length

    @site_length.setter
    def site_length(self, site_length=None):
        if site_length is None:
            site_length = self.pt_connection.get_slot_values(
                self.id, EC.TF_SITE_LENTGH
            )
            if site_length:
                self._site_length = site_length
            else:
                self._site_length = site_length
        else:
            self._site_length = site_length

    @property
    def symmetry(self):
        return self._symmetry

    @symmetry.setter
    def symmetry(self, symmetry=None):
        if symmetry is None:
            symmetry = self.pt_connection.get_slot_values(
                self.id, EC.TF_SYMMETRY
            )
            self._symmetry = symmetry
        else:
            self._symmetry = symmetry

    def get_products_ids(self):
        product_ids = []
        parent_classes = TranscriptionFactor.pt_connection.get_frame_all_parents(
            self.id)
        if EC.POLYPEPTIDE_CLASS in parent_classes or EC.PSEUDO_PRODUCT_CLASS in parent_classes:
            product_ids.append(self.id)
        else:
            tf_monomers = TranscriptionFactor.pt_connection.monomers_of_protein(
                self.id)
            for monomer_id in tf_monomers:
                parent_classes = (
                    TranscriptionFactor.pt_connection.get_frame_all_parents(monomer_id))
                if EC.POLYPEPTIDE_CLASS in parent_classes:
                    product_ids.append(monomer_id)
        return product_ids

    @staticmethod
    def get_tf_active_conformations(transcription_factor_id):
        active_regulator_ids = []
        containers_of_tf = TranscriptionFactor.pt_connection.modified_containers(
            transcription_factor_id)
        for container_of_id in containers_of_tf:
            parent_classes = TranscriptionFactor.pt_connection.get_frame_all_parents(
                container_of_id)
            regulates = TranscriptionFactor.pt_connection.get_slot_values(
                container_of_id, EC.REGULATES_SLOT)
            if regulates and any(protein_class in EC.PROTEIN_CLASSES for protein_class in parent_classes):
                active_regulator_ids.append(container_of_id)
        return active_regulator_ids

    @staticmethod
    def get_tf_inactive_conformations(transcription_factor_id):
        inactive_regulator_ids = []
        containers_of_tf = TranscriptionFactor.pt_connection.modified_containers(
            transcription_factor_id)
        for container_of_id in containers_of_tf:
            parent_classes = TranscriptionFactor.pt_connection.get_frame_all_parents(
                container_of_id)
            regulates = TranscriptionFactor.pt_connection.get_slot_values(
                container_of_id, EC.REGULATES_SLOT)
            if EC.PROTEIN_SMC_CLASS in parent_classes and not regulates:
                inactive_regulator_ids.append(container_of_id)
        return inactive_regulator_ids

    @staticmethod
    def get_protein_function(protein_ris):
        functions = []
        for ri_id in protein_ris:
            function = TranscriptionFactor.pt_connection.get_slot_value(
                ri_id, EC.MODE_SLOT)
            if function is not None:
                if "+" in function:
                    functions.append("activator")
                elif "-" in function:
                    functions.append("repressor")
                else:
                    function.append(None)
        protein_function = TranscriptionFactor.get_absolute_function(functions)
        return protein_function

    @staticmethod
    def get_absolute_function(functions):
        functions = list(set(functions))
        if all(function in functions for function in ["activator", "repressor"]):
            protein_function = "dual"
        elif all("activator" == function for function in functions):
            protein_function = "activator"
        elif all("repressor" == function for function in functions):
            protein_function = "repressor"
        else:
            protein_function = None
        return protein_function

    @property
    def citations(self):
        return self._citations

    @citations.setter
    def citations(self, citations):
        citations = utils.get_citations(citations)
        # print("OLD_CITATIONS: ", citations)
        # print("TF_ID: ", self.id)
        all_conf = (self.get_tf_active_conformations(self.id) +
                    self.get_tf_inactive_conformations(self.id))
        # print("conf_Len: ", len(all_conf))
        for tf_conf in all_conf:
            # print("CLPX_ID: ", tf_conf)
            conf_citations = (TranscriptionFactor.pt_connection.get_slot_values(
                tf_conf, '|CITATIONS|'))
            new_citations = utils.get_citations(conf_citations)
            # print("NEW_CITATIONS: ", new_citations)
            if citations:
                if new_citations:
                    citations.extend(
                        citation for citation in new_citations if citation not in citations)
            elif new_citations:
                citations = new_citations
        # print("CITATIONS: ", citations)
        if not citations:
            citations = None
        self._citations = citations


class TFComplexes(Base):

    def __init__(self, **kwargs):
        super(TFComplexes, self).__init__(**kwargs)
