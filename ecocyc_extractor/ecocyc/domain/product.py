from .base import Base

import pythoncyc

from ..utils import constants as EC
from ..utils import utils


class Product(Base):
    # **kwargs = key word arguments
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)
        self.type_ = None
        self.abbreviated_name = kwargs.get("abbreviated_name", None)
        self.anticodon = kwargs.get("anticodon", None)
        self.catalyzes = kwargs.get("catalyzes", None)
        self.coding_segments = kwargs.get("coding_segments", None)
        self.consensus_sequences = kwargs.get("consensus_sequences", None)
        self.component_of = kwargs.get("component_of", None)
        self.db_links = kwargs.get("dblinks", None)
        self.gene = kwargs.get("gene", None)
        self.isoelectric_points = kwargs.get("isoelectric_point", None)
        self.locations = kwargs.get("locations", None)
        self.modified_forms = kwargs.get("modified_forms", None)
        self.molecular_weight = kwargs.get("molecular_weight", None)
        self.molecular_weights_kd = kwargs.get("molecular_weights_kd", None)
        self.motifs = kwargs.get("features", None)
        self.sequence = None
        self.site_length = kwargs.get("site_length", None)
        self.splice_form_introns = kwargs.get("splice_form_introns", None)
        self.symmetries = kwargs.get("symmetries", None)
        self.terms = kwargs.get("terms", None)

    @property
    def catalyzes(self):
        return self._catalyzes

    @catalyzes.setter
    def catalyzes(self, catalyzes):
        self._catalyzes = []
        try:
            for catalyze_id in catalyzes:
                self._catalyzes.append(
                    self.pt_connection.get_name_by_id(catalyze_id))
            self._catalyzes = list(set(self._catalyzes))
        except TypeError:
            self._catalyzes = None

    @property
    def consensus_sequences(self):
        return self._consensus_sequences

    @consensus_sequences.setter
    def consensus_sequences(self, consensus_sequences):
        self._consensus_sequences = []
        try:
            self._consensus_sequences = [consensus_sequence.strip(
            ) for consensus_sequence in consensus_sequences]
        except TypeError:
            self._consensus_sequences = None

    @property
    def component_of(self):
        return self._component_of

    @component_of.setter
    def component_of(self, component_of):
        self._component_of = []
        try:
            for id_component_of in component_of:
                self.component_of.append(
                    self.pt_connection.get_name_by_id(id_component_of))
        except TypeError:
            self._component_of = None

    @property
    def gene(self):
        return self._gene

    @gene.setter
    def gene(self, gene=None):
        if isinstance(gene, list):
            self._gene = gene[0]
        else:
            self._gene = gene

    @property
    def isoelectric_points(self):
        return self._isoelectric_points

    @isoelectric_points.setter
    def isoelectric_points(self, isoelectric_point=None):
        self._isoelectric_points = isoelectric_point

    @property
    def locations(self):
        return self._locations

    @locations.setter
    def locations(self, locations):
        self._locations = []
        try:
            for location_id in locations:
                self._locations.append(
                    self.pt_connection.get_name_by_id(location_id))
        except TypeError:
            self._locations = None

    @property
    def modified_forms(self):
        return self._modified_forms

    @modified_forms.setter
    def modified_forms(self, modified_forms):
        self._modified_forms = []
        try:
            for id_modified_form_id in modified_forms:
                self._modified_forms.append(
                    self.pt_connection.get_name_by_id(id_modified_form_id))
        except TypeError:
            self._modified_forms = None

    @property
    def name(self):
        if self._name is None:
            try:
                gene_name = self.pt_connection.get_name_by_id(self.gene)
                print('ID: ', self.id, 'GENE: ', gene_name)
                print('ABB_Name: ', self.abbreviated_name)
                self._name = (
                    self.abbreviated_name
                    if self.abbreviated_name is not None
                    else "/".join(self.catalyzes)
                )
                if self.abbreviated_name is None:
                    synonyms = self.synonyms
                    short_name = utils.get_similar_string(gene_name, synonyms)
                    if short_name is None:
                        short_name = min(synonyms, key=len)
                        for synonym in synonyms:
                            if synonym in self._name:
                                short_name = synonym
                                continue
                    else:
                        short_name = short_name[0]
                    self._name = short_name
                print('Final Name: ', self._name)
            except TypeError:
                pass
        return self._name

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence=None):
        if sequence is None:
            if self.type_ is not None:
                sequence = self.pt_connection.get_rna_sequence(self.id)
            else:
                sequence = self.pt_connection.get_protein_sequence(self.id)
        self._sequence = sequence

    @property
    def symmetries(self):
        return self._symmetries

    @symmetries.setter
    def symmetries(self, symmetries):
        try:
            self._symmetries = [
                symmetry.capitalize().replace("|", "") for symmetry in symmetries
            ]
        except TypeError:
            self._symmetries = None

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, terms):
        self._terms = {"biologicalProcess": [],
                       "cellularComponent": [], "molecularFunction": []}
        try:
            terms = sorted(list(set(terms)))
            for term_id in terms:
                term_genbank_feature = None
                try:
                    term_genbank_feature = self.pt_connection.map_go_term_genbank_feature(
                        term_id)
                except pythoncyc.PTools.PToolsError:
                    term_genbank_feature = None
                    print(self.id, term_id)

                term_name = self.pt_connection.get_name_by_id(term_id)
                term_object = {"terms_id": term_id, "terms_name": term_name}

                citations_term = self.pt_connection.get_value_annot_list(
                    self.id, EC.GO_TERMS_SLOT, term_id, EC.CITATIONS_SLOT)
                citations_term = utils.get_citations(citations_term)
                if citations_term is not None:
                    term_object["citations"] = citations_term

                if term_genbank_feature == "go_process":
                    self._terms["biologicalProcess"].append(term_object.copy())
                elif term_genbank_feature == "go_component":
                    self._terms["cellularComponent"].append(term_object.copy())
                elif term_genbank_feature == "go_function":
                    self._terms["molecularFunction"].append(term_object.copy())

            if not self._terms["biologicalProcess"]:
                self._terms["biologicalProcess"] = None
            if not self._terms["cellularComponent"]:
                self._terms["cellularComponent"] = None
            if not self._terms["molecularFunction"]:
                self._terms["molecularFunction"] = None
            self._terms = self.get_only_properties_with_values(self._terms)

        except TypeError:
            self._terms = None

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, product_type=None):
        self._type = None
        if product_type is None:
            rnas_classes = {
                "|All-tRNAs|": "tRNAs",
                "|rRNAs|": "rRNA",
                "|snRNAs|": "snRNA",
                "|tmRNAs|": "tmRNA",
                "|Regulatory-RNAs|": "small RNA",
                "|Misc-RNAs|": "small RNA",
            }
            for rna_class_id, product_type in rnas_classes.items():
                if self.pt_connection.get_instance_all_instance_of_p(self.id, rna_class_id):
                    self._type = product_type
                    break
