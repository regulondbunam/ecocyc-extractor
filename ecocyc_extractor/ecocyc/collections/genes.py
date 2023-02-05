import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.gene import Gene


class Genes(object):
    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = Genes.get_ids(ids)

    @staticmethod
    def get_ids(gene_ids=None):
        if gene_ids is None:
            gene_ids = Genes.pt_connection.get_class_all_instances(
                EC.GENE_CLASS)
        gene_ids = utils.get_unique_elements(gene_ids)
        return gene_ids

    @property
    def objects(self):
        gene_objects = Genes.pt_connection.get_frame_objects(self.ids)
        for gene in gene_objects:
            gene = Genes.set_gene(gene)
            logging.info('Working on gene: {}'.format(gene["id"]))
            ecocyc_gene = Gene(**gene)
            yield ecocyc_gene

    @staticmethod
    def set_gene(gene):
        new_gene = dict(
            id=gene[EC.ID],
            accession_1=gene[EC.ACCESSION_1],
            dblinks=gene[EC.DBLINKS],
            centisome_position=gene[EC.CENTISOME_POSITION],
            citations=gene[EC.CITATIONS],
            comment=gene[EC.COMMENT],
            fragments=gene[EC.FRAGMENTS],
            interrupted=gene[EC.INTERRUPTED],
            internal_comment=gene[EC.INTERNAL_COMMENT],
            lend=gene[EC.LEND],
            name=gene[EC.NAME],
            organism=EC.ORGANISM_ID,
            products=gene[EC.SLOT_PRODUCT_CLASS],
            rend=gene[EC.REND],
            strand=gene[EC.TRANSCRIPTION_DIRECTION_SLOT],
            synonyms=gene[EC.SYNONYMS]
        )
        return new_gene
