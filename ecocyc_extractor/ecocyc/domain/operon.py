from .base import Base
from ..utils import constants as EC
from ..utils import utils
from ..collections.terminators import Terminators
from ..collections.promoters import Promoters


class Operon(object):

    all_terminator_ids = Terminators.get_ids()
    all_promoter_ids = Promoters.get_ids()
    pt_connection = Base.pt_connection

    def __init__(self, **kwargs):
        self.id = kwargs.get("transcription_unit_ids", None)
        self.transcription_unit_ids = kwargs.get("transcription_unit_ids", None)
        self.db_links = kwargs.get("dblinks", None)
        self.genes = kwargs.get("transcription_unit_ids", None)
        self.name = kwargs.get("name", None)
        self.organism = kwargs.get("organism", None)
        self.strand = kwargs.get("strand", None)
        self.regulation_positions = kwargs.get("regulation_positions", None)
    
    @property
    def db_links(self):
        return self._db_links

    @db_links.setter
    def db_links(self, external_cross_references):
        self._db_links = []
        try:
            self._db_links.extend(utils.get_external_cross_references(external_cross_references))
        except TypeError:
            pass
        for tu_id in self.transcription_unit_ids:
            ecocyc_reference = {
                "externalCrossReferences_id": "|ECOCYC|",
                "objectId": tu_id.replace("|", ""),
            }
            if ecocyc_reference not in self._db_links:
                self._db_links.append(ecocyc_reference.copy())
    
    @property
    def id(self):
        return self._formatted_id

    @id.setter
    def id(self, tu_ids):
        self._formatted_id = ";".join(tu_ids)

    @property
    def genes(self):
        return self._genes

    @genes.setter
    def genes(self, genes):
        if genes is not None:
            genes = self.get_transcription_units_genes(self.transcription_unit_ids)
            genes = self.get_genes(genes)
        self._genes = genes

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if name is None:
            name = self.pt_connection.get_operon_name(self.transcription_unit_ids)
        self._name = name

    @property
    def regulation_positions(self):
        return self._regulation_positions

    @regulation_positions.setter
    def regulation_positions(self, regulation_positions=None):
        if regulation_positions is None:
            terminator_ids = self.get_transcription_units_terminators(self.transcription_unit_ids)
            promoter_ids = self.get_transcription_units_promoters(self.transcription_unit_ids)
            site_ids = self.get_transcription_units_sites(self.transcription_unit_ids)
            regulation_positions = self.get_regulation_positions(self.genes, promoter_ids, terminator_ids, site_ids, self.strand)
        self._regulation_positions = regulation_positions

    @property
    def strand(self):
        return self._strand

    @strand.setter
    def strand(self, strand=None):
        if strand is None:
            strand = self.pt_connection.get_transcription_direction(self.transcription_unit_ids[0])
            strand = Base.get_strand(strand)
        self._strand = strand

    @staticmethod
    def get_transcription_units_genes(tu_ids, allow_fragments=False):
        gene_ids = []
        for tu_id in tu_ids:
            tu_gene_ids = Operon.pt_connection.transcription_unit_genes(tu_id)
            gene_ids.extend(tu_gene_ids)
        gene_ids = utils.get_unique_elements(gene_ids)
        return gene_ids

    @staticmethod
    def get_transcription_units_terminators(tu_ids):
        terminator_ids = []
        for tu_id in tu_ids:
            tu_terminator_ids = Operon.pt_connection.transcription_unit_terminators(tu_id)
            terminator_ids.extend(tu_terminator_ids)
        terminator_ids = utils.get_unique_elements(terminator_ids)
        return terminator_ids

    @staticmethod
    def get_transcription_units_promoters(tu_ids):
        promoter_ids = []
        for tu_id in tu_ids:
            tu_promoter_ids = Operon.pt_connection.transcription_unit_promoter(tu_id)
            if tu_promoter_ids:
                promoter_ids.append(tu_promoter_ids)
        promoter_ids = utils.get_unique_elements(promoter_ids)
        return promoter_ids

    @staticmethod
    def get_transcription_units_sites(tu_ids):
        site_ids = []
        for tu_id in tu_ids:
            tu_site_ids = Operon.pt_connection.transcription_unit_binding_sites(tu_id)
            site_ids.extend(tu_site_ids)
        site_ids = utils.get_unique_elements(site_ids)
        return site_ids

    @staticmethod
    def get_genes(gene_ids):
        genes = []
        for gene_id in gene_ids:
            gene_object = {
                "genes_id": gene_id,
                "leftEndPosition": Operon.pt_connection.get_slot_value(gene_id, EC.LEND_SLOT),
                "rightEndPosition": Operon.pt_connection.get_slot_value(gene_id, EC.REND_SLOT)
            }
            if gene_object["leftEndPosition"] is None and gene_object["rightEndPosition"] is None:
                gene_fragments = Operon.pt_connection.get_slot_values(gene_id, EC.FRAGMENTS_SLOT)
                if gene_fragments:
                    lend_positions = []
                    rend_positions = []
                    for gene_fragment_id in gene_fragments:
                        gene_lend_position = Operon.pt_connection.get_slot_value(gene_fragment_id, EC.LEND_SLOT)
                        lend_positions.append(gene_lend_position)
                        gene_rend_position = Operon.pt_connection.get_slot_value(gene_fragment_id, EC.REND_SLOT)
                        rend_positions.append(gene_rend_position)
                    gene_object["leftEndPosition"] = min(lend_positions)
                    gene_object["rightEndPosition"] = max(rend_positions)
            gene_object = Base.get_only_properties_with_values(gene_object)
            if gene_object not in genes:
                genes.append(gene_object.copy())
        return genes

    @staticmethod
    def get_regulation_positions(genes, promoter_ids, terminator_ids, site_ids, strand):
        genes_min_left_position, genes_max_right_position = Operon.get_genes_positions(genes)
        terminators_left_positions, terminators_right_positions = Operon.get_positions(terminator_ids)
        promoters_pos_1s = Operon.get_promoters_pos1_positions(promoter_ids)
        sites_left_positions, sites_right_positions = Operon.get_site_positions(site_ids)

        left_end_positions = [genes_min_left_position]
        right_end_positions = [genes_max_right_position]

        if terminators_right_positions:
            right_end_positions.append(max(terminators_right_positions))
        if sites_right_positions:
            right_end_positions.append(max(sites_right_positions))

        right_end_positions = [rend for rend in right_end_positions if rend]
        # try:
        #    right_end_positions.remove(None)
        # except ValueError:
        #    pass
        right_end_position = max(right_end_positions)

        if terminators_left_positions:
            left_end_positions.append(min(terminators_left_positions))
        if sites_left_positions:
            left_end_positions.append(min(sites_left_positions))

        if promoters_pos_1s:
            left_end_positions.append(min(promoters_pos_1s))

        # try:
        #    left_end_positions.remove(None)
        # except ValueError:
        #    pass
        left_end_positions = [lend for lend in left_end_positions if lend]
        left_end_position = min(left_end_positions)

        regulation_positions = {
            "leftEndPosition": left_end_position,
            "rightEndPosition": right_end_position,
        }

        return regulation_positions

    @staticmethod
    def get_positions(ids):
        left_positions = []
        right_positions = []
        for object_id in ids:
            pos_left = Operon.pt_connection.get_slot_value(object_id, EC.LEND_SLOT)
            pos_right = Operon.pt_connection.get_slot_value(object_id, EC.REND_SLOT)
            if pos_left is not None:
                left_positions.append(pos_left)
            if pos_right is not None:
                right_positions.append(pos_right)
        return left_positions, right_positions

    @staticmethod
    def get_promoters_pos1_positions(promoter_ids):
        promoters_pos1s = []
        for promoter_id in promoter_ids:
            promoter_pos1 = Operon.pt_connection.get_slot_value(promoter_id, EC.ABSOLUTE_PLUS_1_POS_SLOT)
            if promoter_pos1:
                promoters_pos1s.append(promoter_pos1)
        return promoters_pos1s

    @staticmethod
    def get_site_positions(site_ids):
        left_positions = []
        right_positions = []
        for site_id in site_ids:
            pos_left = Operon.pt_connection.get_site_left_position_extended(site_id)
            pos_right = Operon.pt_connection.get_site_right_position_extended(site_id)
            if pos_left is not None:
                left_positions.append(pos_left)
            if pos_right is not None:
                right_positions.append(pos_right)
        return left_positions, right_positions

    @staticmethod
    def get_genes_positions(genes):
        lend_positions = []
        rend_positions = []
        for gene in genes:
            lend_positions.append(gene.get("leftEndPosition", None))
            rend_positions.append(gene.get("rightEndPosition", None))

        return min(lend_positions), max(rend_positions)

    @staticmethod
    def get_only_properties_with_values(properties):
        properties = {k: v for k, v in properties.items() if v is not None}
        return properties