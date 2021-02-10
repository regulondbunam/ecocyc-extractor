from .base import Base
from ..collections.genes import Genes
from ..collections.products import Products
from ..utils import constants as EC
from ..utils import utils


class Term(Base):

    product_ids = Products.get_ids()
    gene_ids = Genes.get_ids()

    def __init__(self, **kwargs):
        super(Term, self).__init__(**kwargs)
        self.db_links = kwargs.get("dblinks", None)
        self.definition = kwargs.get("definition", None)
        self.ontology_id = kwargs.get("ontology_id", None)
        self.parents_ids = kwargs.get("parents_ids", None)
        self.children_ids = kwargs.get("children_ids", None)
        self.members = kwargs.get("term_members", None)

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
    def definition(self):
        return self._definition

    @definition.setter
    def definition(self, definition=None):
        definition = {"text": definition, "source": "EcoCyc"}
        definition = Base.get_only_properties_with_values(definition)
        self._definition = definition

    @property
    def ontology_id(self):
        return self._ontology_id

    @ontology_id.setter
    def ontology_id(self, ontology_id=None):
        if ontology_id is None:
            is_go_term_child = self.pt_connection.child_is_from_parent(
                self.id, EC.GO_TERMS_CLASS
            )
            if is_go_term_child:
                ontology_id = EC.GO_TERMS_CLASS
            else:
                ontology_id = EC.MULTIFUN_CLASS
        self._ontology_id = ontology_id

    @property
    def parents_ids(self):
        return self._parents_ids

    @parents_ids.setter
    def parents_ids(self, parents_ids=None):
        if parents_ids is None:
            parents_ids = self.pt_connection.get_frame_direct_parents(self.id)
        if not parents_ids:
            parents_ids = None
        self._parents_ids = parents_ids

    @property
    def children_ids(self):
        return self._children_ids

    @children_ids.setter
    def children_ids(self, children_ids=None):
        if children_ids is None:
            children_ids = self.pt_connection.get_class_direct_subs(self.id)
        if not children_ids:
            children_ids = None
        self._children_ids = children_ids

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, members=None):
        registered_members = {}
        if members is None:
            if self.ontology_id == EC.MULTIFUN_CLASS:
                members = self.pt_connection.get_class_direct_instances(self.id)
        if members is not None:
            for member_id in members:
                if self.ontology_id == EC.MULTIFUN_CLASS:
                    if member_id in Term.gene_ids:
                        registered_members.setdefault("genes", []).append(member_id)
                elif self.ontology_id == EC.GO_TERMS_CLASS:
                    if member_id in Term.product_ids:
                        registered_members.setdefault("products", []).append(member_id)
        if not registered_members:
            registered_members = None
        self._members = registered_members
