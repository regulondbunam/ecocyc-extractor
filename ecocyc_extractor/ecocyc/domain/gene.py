from .base import Base
from ..utils import constants as EC
from ..utils import utils


class Gene(Base):
    # **kwargs: key word arguments
    def __init__(self, **kwargs):
        super(Gene, self).__init__(**kwargs)
        self.centisome_position = kwargs.get("centisome_position", None)
        self.db_links = kwargs.get("dblinks", None)
        self._fragments = kwargs.get("fragments", None)
        self._gc_content = kwargs.get("gc_content", None)
        self._products = kwargs.get("products", None)
        self.sequence = kwargs.get("sequence", None)
        self.synonyms = kwargs.get("synonyms", None)
        self.type = kwargs.get("type", None)
        self.terms = kwargs.get("terms", None)
        self.name = kwargs.get("name", None)

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
            "objectId": self.id.replace("|", "")
        }
        self._db_links.append(ecocyc_reference.copy())

        if self.bnumber:
            bnumber_reference = {
                "externalCrossReferences_id": "|REFSEQ|",
                "objectId": self.bnumber
            }
            self._db_links.append(bnumber_reference.copy())

    @property
    def fragments(self):
        fragments = []
        if self._fragments is not None:
            fragment_objects = self.pt_connection.get_frame_objects(
                self._fragments)
            for fragment_object in fragment_objects:
                new_fragment_object = {
                    'id': fragment_object[EC.ID],
                    'centisomePosition': fragment_object[EC.CENTISOME_POSITION],
                    'name': fragment_object[EC.NAME],
                    'leftEndPosition': fragment_object[EC.LEND],
                    'rightEndPosition': fragment_object[EC.REND],
                    'sequence': self.pt_connection.get_gene_sequence(fragment_object[EC.ID]),
                    'strand': self.get_strand(fragment_object[EC.TRANSCRIPTION_DIRECTION])
                }
                # This will drop any key whose value is None
                new_fragment_object_filtered = {
                    k: v for k, v in new_fragment_object.items() if v is not None}
                fragments.append(new_fragment_object_filtered.copy())
        if not fragments:
            fragments = None
        return fragments

    @property
    def gc_content(self):
        self._gc_content = None
        if self._sequence is not None and self._gc_content is None:
            format_value = "%.2f"
            self._gc_content = self.sequence.count(
                'C') + self.sequence.count('G')
            self._gc_content = (
                (float(self._gc_content) * 100) / len(self.sequence))
            # self._gc_content = format_value % self._gc_content
        return self._gc_content

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name is None:
            name = self.id.replace("|", "")
        self._name = name

    @property
    def products(self):
        products = []
        if self._products is not None:
            product_classes = [EC.POLYPEPTIDE_CLASS,
                               EC.PSEUDO_PRODUCT_CLASS, EC.RNAS]
            for product_id in self._products:
                object_classes = self.pt_connection.get_frame_all_parents(
                    product_id)
                unmodified_form = self.pt_connection.get_slot_value(
                    product_id, EC.SLOT_UNMODIFIED_FORM_CLASS)
                # Validating if the protein is from the previous given classes and if it is not a modified form
                if any(product_class in product_classes for product_class in
                       object_classes) and unmodified_form is None:
                    products.append(product_id)
        if not products:
            products = None
        return products

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence=None):
        if sequence is None:
            self._sequence = self.pt_connection.get_gene_sequence(self.id)
        else:
            self._sequence = sequence

    @property
    def synonyms(self):
        return self._synonyms

    @synonyms.setter
    def synonyms(self, synonyms=None):
        gene_id = self.id.replace("|", "")
        self._synonyms = synonyms
        try:
            self._synonyms.append(gene_id)
        except AttributeError:
            self._synonyms = [gene_id]

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, gene_physiological_roles=None):
        terms = []
        if not gene_physiological_roles:
            gene_physiological_roles = self.pt_connection.physiological_roles_of_gene(
                self.id)
        for role_id in gene_physiological_roles:
            role_parent_classes = self.pt_connection.get_frame_all_parents(
                role_id)
            role_name = self.pt_connection.get_name_by_id(role_id)

            term_object = {}
            term_object.setdefault('terms_id', role_id)
            term_object.setdefault('terms_name', role_name)

            labels = []
            for parent_class_id in role_parent_classes[7:]:
                name_parent_class = self.pt_connection.get_name_by_id(
                    parent_class_id)
                term_parent_object = {
                    "terms_id": parent_class_id,
                    "terms_name": name_parent_class
                }
                term_object.setdefault('parents', []).append(
                    term_parent_object.copy())

                parent_label = " - ".join([parent_class_id.replace(
                    "|", "").replace("BC-", ""), name_parent_class])
                labels.append(parent_label)

            term_label = " - ".join([role_id.replace("|",
                                                     "").replace("BC-", ""), role_name])
            labels.append(term_label)
            labels = " --> ".join(labels)
            term_object.setdefault('termLabel', labels)

            terms.append(term_object.copy())
        self._terms = list(terms)
        if not self._terms:
            self._terms = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type=None):
        if _type is None:
            self._type = None
            if self.pt_connection.pseudo_gene_p(self.id):
                self._type = "pseudo"
            elif self.pt_connection.phantom_gene_p(self.id):
                self._type = "phantom"
        else:
            self._type = _type

    def __len__(self):
        return self.left_end_position - self.right_end_position if self.strand == "reverse" else self.right_end_position - self.left_end_position
