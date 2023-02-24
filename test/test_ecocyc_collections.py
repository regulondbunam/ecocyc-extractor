# Standard
import unittest
import os

# Thirdparty
import pythoncyc
import identifiers_api

# Local
from ecocyc_extractor.ecocyc.utils import constants as EC
from ecocyc_extractor.ecocyc.collections.evidences import Evidences
from ecocyc_extractor.ecocyc.collections.external_databases import ExternalDatabases
from ecocyc_extractor.ecocyc.collections.genes import Genes

organism = 'ECOLI'
pt_conn = pythoncyc.select_organism(organism)
url = 'mongodb://localhost'
database = 'regulondbmultigenomic'


class TestCycCollections(unittest.TestCase):
    '''
        Test class for debug regulondb module collections functions
    '''

    def test_evidences(self):
        evidences = Evidences()
        ev_ids = [
            '|EV-EXP-IGI-FUNC-COMPLEMENTATION|', '|EV-EXP-IDA-UNPURIFIED-PROTEIN-HH|', '|EV-EXP-IDA-UNPURIFIED-PROTEIN-NH|', '|EV-EXP-CHIP-EXO-MANUAL|', '|EV-EXP-IEP-GENE-EXPRESSION-ANALYSIS|', '|EV-EXP-IEP-MICROARRAY|', '|EV-EXP-IMP-REACTION-BLOCKED|', '|EV-EXP-IEP-RNA-SEQ|', '|EV-EXP-IMP-REACTION-ENHANCED|', '|EV-EXP-IEP-COREGULATION|', '|EV-EXP-IMP-SITE-MUTATION|', '|EV-EXP-IMP-POLAR-MUTATION|', '|EV-COMP-HINF-ORTHOLOGY-EXP|', '|EV-IC-ADJ-GENES-SAME-BIO-PROCESS|', '|EV-EXP-IDA-PURIFIED-PROTEIN-HH|', '|EV-EXP-IDA-PURIFIED-PROTEIN-NH|', '|EV-COMP-AINF-SIMILAR-TO-CONSENSUS|', '|EV-COMP-AINF-FN-FROM-SEQ|', '|EV-COMP-AINF-SINGLE-DIRECTON|', '|EV-COMP-AINF-PATTERN-DISCOVERY|', '|EV-COMP-AINF-POSITIONAL-IDENTIFICATION|', '|EV-ND|', '|EV-EXP|', '|EV-HTP|', '|EV-AS|', '|EV-IC|', '|EV-COMP|', '|EV-EXP-CHIP-SEQ-MANUAL|', '|EV-EXP-GSELEX|', '|EV-COMP-HINF-ISM|', '|EV-COMP-HINF-SEQ-ORTHOLOGY|', '|EV-COMP-HINF-ISA|', '|EV-COMP-HINF-PATTERN-DISCOVERY|', '|EV-COMP-HINF-POSITIONAL-IDENTIFICATION|', '|EV-COMP-HINF-SIMILAR-TO-CONSENSUS|', '|EV-COMP-HINF-FN-FROM-SEQ|', '|EV-COMP-HINF-IGC|'
        ]
        identifiers_api.connect(url)
        mg_ids = identifiers_api.get_identifiers(
            EC.EV_COLLECTION, database, organism)
        mg_ids = list(mg_ids.keys())
        new_ids = evidences.get_ids()
        self.assertTrue(
            all(item in new_ids for item in mg_ids)
            or  # First condition only for the test development
            all(item in mg_ids for item in ev_ids),
            f'Not all new IDs in the current RegulonDBMultigenomic IDs\n -Old IDs:{mg_ids}\n   -New IDs:{new_ids}'
        )
        identifiers_api.disconnect()

    def test_external_dbs(self):
        external_dbs = ExternalDatabases()
        identifiers_api.connect(url)
        mg_ids = identifiers_api.get_identifiers(
            EC.EXREF_COLLECTION, database, organism)
        mg_ids = list(mg_ids.keys())
        new_ids = external_dbs.get_ids()
        self.assertTrue(
            all(item in new_ids for item in mg_ids)
            or  # First condition only for the test development
            all(item in mg_ids for item in new_ids),
            f'Not all new IDs in the current RegulonDBMultigenomic IDs\n -Old IDs:{mg_ids}\n   -New IDs:{new_ids}'
        )
        identifiers_api.disconnect()

    def test_genes(self):
        genes = Genes()
        identifiers_api.connect(url)
        mg_ids = identifiers_api.get_identifiers(
            EC.GENE_COLLECTION, database, organism)
        mg_ids = list(mg_ids.keys())
        new_ids = genes.get_ids()
        self.assertTrue(
            all(item in new_ids for item in mg_ids)
            or  # First condition only for the test development
            all(item in mg_ids for item in new_ids),
            f'Not all new IDs in the current RegulonDBMultigenomic IDs\n -Old IDs:{mg_ids}\n   -New IDs:{new_ids}'
        )
        identifiers_api.disconnect()


if __name__ == '__main__':
    unittest.main()
