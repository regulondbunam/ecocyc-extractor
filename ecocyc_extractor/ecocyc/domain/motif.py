from ecocyc_extractor.ecocyc.collections.products import Products
from .base import Base
from .product import Product
from ..utils import constants as EC
from ..utils import utils


class Motif(Base):

    _gene_product_ids = Products.get_ids()
    products = {}

    def __init__(self, **kwargs):
        super(Motif, self).__init__(**kwargs)
        self.alternate_sequence = kwargs.get("alternate_sequence", None)
        self.attached_group = kwargs.get("attached_group", None)
        self.db_links = kwargs.get("dblinks", None)
        self.class_ = kwargs.get("class", None)
        self.data_source = kwargs.get("data_source", None)
        self.description = kwargs.get("name", None)
        self.feature_color = kwargs.get("feature_color", None)
        self.homology_motif = kwargs.get("homology_motif", None)
        self.product_id = kwargs.get("products", None)
        self._sequence = kwargs.get("sequence", None)
        self.residue_number = kwargs.get("residue_number", None)
        self.type_ = kwargs.get("type", None)

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
    def attached_group(self):
        return self._attached_group

    @attached_group.setter
    def attached_group(self, groups=None):
        try:
            names = []
            for group_id in groups:
                if " " not in group_id:
                    names.append(self.pt_connection.get_name_by_id(group_id))
            self._attached_group = ", ".join(names)
        except TypeError:
            self._attached_group = None

        if not self._attached_group:
            self._attached_group = None

    @property
    def class_(self):
        return self._class

    @class_.setter
    def class_(self, class_=None):
        if class_ is None:
            self._class = self.pt_connection.get_feature_class_name(self.id)
        else:
            self._class = class_

    @property
    def feature_color(self):
        return self._feature_color

    @feature_color.setter
    def feature_color(self, feature_color=None):
        if feature_color is not None:
            feature_color = feature_color.replace("|", "").lower()
        self._feature_color = feature_color

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_ids):
        self._product_id = self.get_feature_of(product_ids, self._gene_product_ids)

    @property
    def sequence(self):
        if self._sequence is None:

            product = Motif.get_product(self.product_id)
            # Since there are products that have no sequence, we catch them in the
            # except block and set the motif sequence as None.
            try:
                if self.left_end_position and self.right_end_position:
                    if self.left_end_position == self.right_end_position:
                        self._sequence = product.sequence[self.left_end_position - 1 : self.right_end_position]
                    else:
                        self._sequence = product.sequence[self.left_end_position : self.right_end_position]
                else:
                    if self.residue_number:
                        self._sequence = product.sequence[self.residue_number[0] - 1]
            except TypeError:
                self._sequence = None
        return self._sequence

    @classmethod
    def get_product(cls, product_id):
        return cls.products.setdefault(product_id, Product(**dict(id=product_id)))

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, type_=None):
        if type_ is None and self.data_source is not None:
            if "pfam" in self.data_source.lower():
                self._type = "Pfam"
            elif "uniprot" in self.data_source.lower():
                self._type = "UniProt"
            else:
                self._type = None
        else:
            self._type = type_

    @staticmethod
    def get_feature_of(feature_of, gene_product_ids):
        """
        Removes the polypeptide identifiers that are not been processed as products in the extraction,
        resulting in only one product identifier.
        :param feature_of: Polypeptide identifiers of the motif, some identifiers might not be part of the process.
        :param gene_product_ids: Identifiers of products that are going to be processed.
        :return motif_product_id: Product identifiers of the related motif and that are going to be processed
        """
        motif_product_id = None
        for product_id in feature_of:
            if product_id in gene_product_ids:
                motif_product_id = product_id
                break
        return motif_product_id
