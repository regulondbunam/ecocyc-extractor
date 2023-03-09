import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.product import Product
from .genes import Genes


class Products(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = Products.get_ids(ids)

    @staticmethod
    def get_ids(product_ids=None):
        if product_ids is None:
            product_ids = []
            gene_ids = Genes.get_ids()
            # In order to accept if a protein_id is a product_id, the first rule is to be part of one of these classes
            product_classes = [EC.POLYPEPTIDE_CLASS, EC.PSEUDO_PRODUCT_CLASS, EC.RNAS]
            for gene_id in gene_ids:
                polypeptide_ids = Products.pt_connection.get_slot_values(gene_id, EC.SLOT_PRODUCT_CLASS)
                for polypeptide_id in polypeptide_ids:
                    object_classes = Products.pt_connection.get_frame_all_parents(polypeptide_id)
                    unmodified_form = Products.pt_connection.get_slot_value(polypeptide_id, EC.SLOT_UNMODIFIED_FORM_CLASS)
                    # Validating if the protein is from the previous given classes and if it is not a modified form
                    if any(product_class in product_classes for product_class in object_classes) and unmodified_form is None:
                        product_ids.append(str(polypeptide_id))
        product_ids = utils.get_unique_elements(product_ids)
        return product_ids

    @property
    def objects(self):
        product_objects = Products.pt_connection.get_frame_objects(self.ids)
        for product in product_objects:
            product = Products.set_product(product)
            logging.info('Working on product: {}'.format(product["id"]))
            ecocyc_product = Product(**product)
            yield ecocyc_product

    @staticmethod
    def set_product(product):
        new_product = dict(
            id=product[EC.ID],
            abbreviated_name=product[EC.ABBREV_NAME],
            anticodon=product[EC.ANTICODON],
            catalyzes=product[EC.CATALYZES],
            citations=product[EC.CITATIONS],
            coding_segments=product[EC.CODING_SEGMENTS],
            comment=product[EC.COMMENT],
            component_of=product[EC.COMPONENT_OF],
            consensus_sequences=product[EC.CONSENSUS_SEQUENCE],
            dblinks=product[EC.DBLINKS],
            features=product[EC.FEATURES],
            gene=product[EC.GENE],
            internal_comment=product[EC.INTERNAL_COMMENT],
            isoelectric_point=product[EC.ISOELECTRIC_POINT],
            locations=product[EC.LOCATIONS],
            modified_forms=product[EC.MODIFIED_FORM],
            molecular_weight=product[EC.MOLECULAR_WEIGHT_SEQ],
            molecular_weights_kd=product[EC.MOLECULAR_WEIGHT_KD],
            name=product[EC.NAME],
            organism=EC.ORGANISM_ID,
            site_length=product[EC.DNA_FOOTPRINT_SIZE],
            splice_form_introns=product[EC.SPLICE_FORM_INTRONS],
            symmetries=product[EC.SYMMETRY],
            synonyms=product[EC.SYNONYMS],
            terms=product[EC.GO_TERMS]
        )
        return new_product
