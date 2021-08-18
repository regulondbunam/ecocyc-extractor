import logging

from ecocyc.utils.pathway_tools.connection import Connection
from ecocyc.utils import constants as EC, utils
from ecocyc.domain.motif import Motif
from .products import Products


class Motifs(object):

    pt_connection = Connection()
    product_ids = Products.get_ids()

    def __init__(self, ids=None):
        self.ids = Motifs.get_ids(ids, Motifs.product_ids)

    @staticmethod
    def get_ids(motif_ids=None, product_ids=None):
        if product_ids is None:
            product_ids = Products.get_ids()

        if motif_ids is None:
            motif_ids = []
            for product_id in product_ids:
                feature_ids = Motifs.pt_connection.get_slot_values(product_id, EC.SLOT_FEATURE_CLASS)
                if feature_ids:
                    motif_ids.extend(feature_ids)
        motif_ids = utils.get_unique_elements(motif_ids)
        return motif_ids

    @property
    def objects(self):
        motif_objects = Motifs.pt_connection.get_frame_objects(self.ids)
        for motif in motif_objects:
            motif = Motifs.set_motif(motif)
            logging.info('Working on motif: {}'.format(motif["id"]))
            ecocyc_motif = Motif(**motif)
            yield ecocyc_motif

    @staticmethod
    def set_motif(motif):
        new_motif = dict(
            id=motif[EC.ID],
            alternate_sequence=motif[EC.ALTERNATE_SEQUENCE],
            attached_group=motif[EC.ATTACHED_GROUP],
            comment=motif[EC.COMMENT],
            data_source=motif[EC.DATA_SOURCE],
            dblinks=motif[EC.DBLINKS],
            feature_color=motif[EC.FEATURE_COLOR],
            homology_motif=motif[EC.HOMOLOGY_MOTIF],
            internal_comment=motif[EC.INTERNAL_COMMENT],
            lend=motif[EC.LEND],
            name=motif[EC.NAME],
            organism=EC.ORGANISM_ID,
            products=motif[EC.FEATURE_OF],
            rend=motif[EC.REND],
            residue_number=motif[EC.RESIDUE_NUMBER],
            synonyms=motif[EC.SYNONYMS],
            type=None
        )
        return new_motif
