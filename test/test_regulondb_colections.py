# Standard
import unittest

# Thirdparty

# Local
from ecocyc_extractor.regulondb.evidences import get_regulondb_evidences
from ecocyc_extractor.regulondb.external_cross_references import get_regulondb_external_databases
from ecocyc_extractor.regulondb.genes import get_regulondb_genes
from ecocyc_extractor.regulondb.motifs import get_regulondb_motifs
from ecocyc_extractor.regulondb.ontologies import get_regulondb_ontologies
from ecocyc_extractor.regulondb.operons import get_regulondb_operons
from ecocyc_extractor.regulondb.operons import get_regulondb_operons
from ecocyc_extractor.regulondb.products import get_regulondb_products
from ecocyc_extractor.regulondb.promoters import get_regulondb_promoters
from ecocyc_extractor.regulondb.publications import get_regulondb_publications
from ecocyc_extractor.regulondb.regulatory_complexes import get_regulondb_regulatory_complexes
from ecocyc_extractor.regulondb.regulatory_continuants import get_regulondb_regulatory_continuants
from ecocyc_extractor.regulondb.regulatory_interactions import get_regulondb_regulatory_interactions
from ecocyc_extractor.regulondb.segments import get_regulondb_segments
from ecocyc_extractor.regulondb.sigma_factors import get_regulondb_sigma_factors
from ecocyc_extractor.regulondb.terminators import get_regulondb_terminators
from ecocyc_extractor.regulondb.terms import get_regulondb_terms
from ecocyc_extractor.regulondb.transcription_factor_regulatory_sites import get_regulondb_transcription_factor_regulatory_sites
from ecocyc_extractor.regulondb.transcription_factors import get_regulondb_transcription_factors
from ecocyc_extractor.regulondb.transcription_units import get_regulondb_transcription_units


class TestRDBCollections(unittest.TestCase):
    '''
        Test class for debug regulondb module collections functions
        Please set environment variables
            export ORGANISM="ECOLI"
    '''

    def test_evidences(self):
        evidences = get_regulondb_evidences(only_properties_with_values=True)
        self.assertTrue(
            evidences,
            'evidences function is not working properly'
        )

    def test_external_cross_references(self):
        external_cross_references = get_regulondb_external_databases(
            only_properties_with_values=True)
        self.assertTrue(
            external_cross_references,
            'external_cross_references function is not working properly'
        )

    def test_genes(self):
        genes = get_regulondb_genes(only_properties_with_values=True)
        self.assertTrue(
            genes,
            'genes function is not working properly'
        )

    def test_motifs(self):
        motifs = get_regulondb_motifs(only_properties_with_values=True)
        self.assertTrue(
            motifs,
            'motifs function is not working properly'
        )

    def test_ontologies(self):
        ontologies = get_regulondb_ontologies(only_properties_with_values=True)
        self.assertTrue(
            ontologies,
            'ontologies function is not working properly'
        )

    def test_operons(self):
        operons = get_regulondb_operons(only_properties_with_values=True)
        self.assertTrue(
            operons,
            'operons function is not working properly'
        )

    def test_products(self):
        products = get_regulondb_products(only_properties_with_values=True)
        self.assertTrue(
            products,
            'products function is not working properly'
        )

    def test_promoters(self):
        promoters = get_regulondb_promoters(only_properties_with_values=True)
        self.assertTrue(
            promoters,
            'promoters function is not working properly'
        )

    def test_publications(self):
        publications = get_regulondb_publications(
            only_properties_with_values=True)
        self.assertTrue(
            publications,
            'publications function is not working properly'
        )

    def test_regulatory_complexes(self):
        regulatory_complexes = get_regulondb_regulatory_complexes(
            only_properties_with_values=True)
        self.assertTrue(
            regulatory_complexes,
            'regulatory_complexes function is not working properly'
        )

    def test_regulatory_continuants(self):
        regulatory_continuants = get_regulondb_regulatory_continuants(
            only_properties_with_values=True)
        self.assertTrue(
            regulatory_continuants,
            'regulatory_continuants function is not working properly'
        )

    def test_regulatory_interactions(self):
        regulatory_interactions = get_regulondb_regulatory_interactions(
            only_properties_with_values=True)
        self.assertTrue(
            regulatory_interactions,
            'regulatory_interactions function is not working properly'
        )

    def test_segments(self):
        segments = get_regulondb_segments(
            only_properties_with_values=True)
        self.assertTrue(
            segments,
            'segments function is not working properly'
        )

    def test_sigma_factors(self):
        sigma_factors = get_regulondb_sigma_factors(
            only_properties_with_values=True)
        self.assertTrue(
            sigma_factors,
            'sigma_factors function is not working properly'
        )

    def test_terminators(self):
        terminators = get_regulondb_terminators(
            only_properties_with_values=True)
        self.assertTrue(
            terminators,
            'terminators function is not working properly'
        )

    def test_terms(self):
        terms = get_regulondb_terms(
            only_properties_with_values=True)
        self.assertTrue(
            terms,
            'terms function is not working properly'
        )

    def test_transcription_factor_regulatory_sites(self):
        transcription_factor_regulatory_sites = get_regulondb_transcription_factor_regulatory_sites(
            only_properties_with_values=True)
        self.assertTrue(
            transcription_factor_regulatory_sites,
            'transcription_factor_regulatory_sites function is not working properly'
        )

    def test_transcription_factors(self):
        transcription_factors = get_regulondb_transcription_factors(
            only_properties_with_values=True)
        self.assertTrue(
            transcription_factors,
            'transcription_factors function is not working properly'
        )

    def test_transcription_units(self):
        transcription_units = get_regulondb_transcription_units(
            only_properties_with_values=True)
        self.assertTrue(
            transcription_units,
            'transcription_units function is not working properly'
        )


if __name__ == '__main__':
    unittest.main()
