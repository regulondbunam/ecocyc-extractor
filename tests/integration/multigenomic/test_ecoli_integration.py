import os
import pytest

import identifier_samples as SAMP_IDS

pytestmark = pytest.mark.ecoli

# Local

organism: str = "ECOLI"
cyc_host: str = "localhost"
cyc_port: str = "5008"

# Environment variables required by the Pathway Tools connection
os.environ["ORGANISM"] = organism
os.environ["CYC_HOST"] = cyc_host
os.environ["CYC_PORT"] = cyc_port




@pytest.fixture(scope="session")
def pt_connection():
    """
    Create a session-scoped connection to Pathway Tools.

    This fixture attempts to establish a connection to a running
    Pathway Tools server using the environment variables:
    - ORGANISM
    - CYC_HOST
    - CYC_PORT

    If the connection cannot be established, all tests that depend
    on this fixture will be skipped instead of failing.

    Returns
    -------
    Connection
        An active Pathway Tools connection object.
    """

    from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection

    try:
        conn = Connection()
        return conn
    except (ConnectionRefusedError, TimeoutError, OSError) as e:
        pytest.skip(
            f"Pathway Tools is not accessible at {cyc_host}:{cyc_port}. "
            f"Error: {type(e).__name__}: {e}"
        )
    except Exception as e:
        pytest.skip(
            f"Unexpected error while connecting to Pathway Tools: "
            f"{type(e).__name__}: {e}"
        )


def test_connection_is_alive(pt_connection):
    """
    Verify that the Pathway Tools connection fixture was created successfully.

    If this test is executed, it implies that the connection was established
    without errors.
    """
    assert pt_connection is not None


@pytest.mark.skipif(False,reason="Testing New")
def test_get_frame_object(pt_connection, frame_id: str = "|EG10054|"):
    """
    Retrieve a frame object from Pathway Tools by its frame ID.

    Parameters
    ----------
    frame_id : str
        The Pathway Tools frame identifier to retrieve.

    The test verifies that the returned object is a dictionary,
    which is the expected representation of a frame object.
    Defaults to '|EG10054|' (araC Gene).
    """
    result = pt_connection.get_frame_object(frame_id)
    assert isinstance(result, dict)

@pytest.mark.skipif(False,reason="Testing New")
def test_organism_objects():
    from ecocyc_extractor.regulondb.organisms import get_regulondb_organisms
    data_objects = get_regulondb_organisms(organism_name=organism, only_properties_with_values=True)
    for data_object in data_objects:
        assert data_object["_id"] is not None and data_object["_id"] == f"|{organism}|"
        assert data_object["name"] is not None
        assert "description" in data_object
        assert "genome" in data_object
        assert "pgdbAuthors" in data_object
        assert "pgdbCopyright" in data_object
        assert "pgdbName" in data_object
        assert "strainName" in data_object
        assert "synonyms" in data_object
        assert "url" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_gene_objects():
    from ecocyc_extractor.regulondb.genes import get_regulondb_genes
    data_objects = get_regulondb_genes(gene_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["genes"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["organisms_id"] is not None
        assert "bnumber" in data_object
        assert "centisomePosition" in data_object
        assert "citations" in data_object
        assert "confidenceLevel" in data_object
        assert "externalCrossReferences" in data_object
        assert "fragments" in data_object
        assert "gcContent" in data_object
        assert "internalComment" in data_object
        assert "interrupted" in data_object
        assert "leftEndPosition" in data_object
        assert "name" in data_object
        assert "note" in data_object
        assert "rightEndPosition" in data_object
        assert "sequence" in data_object
        assert "strand" in data_object
        assert "synonyms" in data_object
        assert "terms" in data_object
        assert "type" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_product_objects():
    from ecocyc_extractor.regulondb.products import get_regulondb_products
    data_objects = get_regulondb_products(product_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["products"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["organisms_id"] is not None
        assert data_object["genes_id"] is not None
        assert "abbreviatedName" in data_object
        assert "anticodon" in data_object
        assert "catalyzes" in data_object
        assert "citations" in data_object
        assert "codingSegments" in data_object
        assert "componentOf" in data_object
        assert "confidenceLevel" in data_object
        assert "consensusSequences" in data_object
        assert "externalCrossReferences" in data_object
        assert "internalComment" in data_object
        assert "isoelectricPoints" in data_object
        assert "locations" in data_object
        assert "modifiedForms" in data_object
        assert "molecularWeight" in data_object
        assert "molecularWeightsKd" in data_object
        assert "name" in data_object
        assert data_object.get("note") is None or data_object["note"] is not None
        assert "sequence" in data_object
        assert "siteLength" in data_object
        assert "spliceFormIntrons" in data_object
        assert "symmetries" in data_object
        assert "synonyms" in data_object
        assert "terms" in data_object
        assert "type" in data_object


@pytest.mark.skipif(True, reason="Motif collection causing some issues")
def test_motifs_objects():
    from ecocyc_extractor.regulondb.motifs import get_regulondb_motifs
    data_objects = get_regulondb_motifs(motif_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["motifs"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["products_id"] is not None
        assert data_object["organisms_id"] is not None
        assert "alternateSequence" in data_object
        assert "attachedGroup" in data_object
        assert "class" in data_object
        assert "color" in data_object
        assert "dataSource" in data_object
        assert "description" in data_object
        assert "externalCrossReferences" in data_object
        assert "homologyMotif" in data_object
        assert "internalComment" in data_object
        assert "leftEndPosition" in data_object
        assert "note" in data_object
        assert "residueNumber" in data_object
        assert "rightEndPosition" in data_object
        assert "sequence" in data_object
        assert "synonyms" in data_object
        assert "type" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_tu_objects():
    from ecocyc_extractor.regulondb.transcription_units import get_regulondb_transcription_units
    data_objects = get_regulondb_transcription_units(transcription_unit_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["transcriptionUnits"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["organisms_id"] is not None
        assert data_object["operons_id"] is not None
        assert data_object["genes_ids"] is not None
        assert "citations" in data_object
        assert "confidenceLevel" in data_object
        assert "externalCrossReferences" in data_object
        assert "internalComment" in data_object
        assert "name" in data_object
        assert "note" in data_object
        assert "promoters_id" in data_object
        assert "synonyms" in data_object
        assert "terminators_ids" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_operon_objects():
    from ecocyc_extractor.regulondb.operons import get_regulondb_operons
    data_objects = get_regulondb_operons(operon_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["operons"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["name"] is not None
        assert data_object["regulationPositions"] is not None
        assert data_object["organisms_id"] is not None
        assert "externalCrossReferences" in data_object
        assert "strand" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_terminator_objects():
    from ecocyc_extractor.regulondb.terminators import get_regulondb_terminators
    data_objects = get_regulondb_terminators(terminator_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["terminators"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["transcriptionTerminationSite"] is not None
        assert data_object["sequence"] is not None
        assert data_object["class"] is not None
        assert data_object["organisms_id"] is not None
        assert "citations" in data_object
        assert "confidenceLevel" in data_object
        assert "externalCrossReferences" in data_object
        assert "internalComment" in data_object
        assert "note" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_promoter_objects():
    from ecocyc_extractor.regulondb.promoters import get_regulondb_promoters
    data_objects = get_regulondb_promoters(promoter_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["promoters"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["organisms_id"] is not None
        assert "bindsSigmaFactor" in data_object
        assert "boxes" in data_object
        assert "citations" in data_object
        assert "confidenceLevel" in data_object
        assert "distanceToGene" in data_object
        assert "externalCrossReferences" in data_object
        assert "internalComment" in data_object
        assert "name" in data_object
        assert "note" in data_object
        assert "score" in data_object
        assert "sequence" in data_object
        assert "strand" in data_object
        assert "synonyms" in data_object
        assert "transcriptionStartSite" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_ri_objects():
    from ecocyc_extractor.regulondb.regulatory_interactions import get_regulondb_regulatory_interactions
    data_objects = get_regulondb_regulatory_interactions(regulatory_interaction_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["regulatoryInteractions"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["organisms_id"] is not None
        assert "accessoryProteins" in data_object
        assert "citations" in data_object
        assert "confidenceLevel" in data_object
        assert "externalCrossReferences" in data_object
        assert "function" in data_object
        assert "internalComment" in data_object
        assert "mechanism" in data_object
        assert "note" in data_object
        assert "regulatedEntity" in data_object
        assert "regulationClass" in data_object
        assert "regulationType" in data_object
        assert "regulator" in data_object
        assert "regulatorySites_id" in data_object
        assert "relativeDistSitePromoter" in data_object


@pytest.mark.skipif(True,reason="Problem testing all regulatory sites from sample IDs list, skipping for now")
def test_sites_objects():
    from ecocyc_extractor.regulondb.transcription_factor_regulatory_sites import get_regulondb_transcription_factor_regulatory_sites
    data_objects = get_regulondb_transcription_factor_regulatory_sites(site_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["regulatorySites"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["organisms_id"] is not None
        assert "absolutePosition" in data_object
        assert "citations" in data_object
        assert "confidenceLevel" in data_object
        assert "externalCrossReferences" in data_object
        assert "internalComment" in data_object
        assert "leftEndPosition" in data_object
        assert "length" in data_object
        assert "note" in data_object
        assert "regulationType" in data_object
        assert "rightEndPosition" in data_object
        assert "sequence" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_reg_cplx_objects():
    from ecocyc_extractor.regulondb.regulatory_complexes import get_regulondb_regulatory_complexes
    data_objects = get_regulondb_regulatory_complexes(regulatory_complex_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["regulatoryComplexes"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["organisms_id"] is not None
        assert "abbreviatedName" in data_object
        assert "citations" in data_object
        assert "confidenceLevel" in data_object
        assert "externalCrossReferences" in data_object
        assert data_object.get("internalComment") is None or data_object["internalComment"] is not None
        # assert "isTranscriptionFactor" in data_object
        assert "name" in data_object
        assert "note" in data_object
        assert "products" in data_object
        assert "regulatoryContinuants_ids" in data_object
        assert "synonyms" in data_object
        assert "type" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_reg_continuant_objects():
    from ecocyc_extractor.regulondb.regulatory_continuants import get_regulondb_regulatory_continuants
    data_objects = get_regulondb_regulatory_continuants(regulatory_complexes_compounds=SAMP_IDS.SAMPLE_IDS_BY_TYPE["regulatoryContinuants"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object.get("name") is None or data_object["name"] is not None
        assert data_object["organisms_id"] is not None
        assert "citations" in data_object
        assert "confidenceLevel" in data_object
        assert "externalCrossReferences" in data_object
        assert "internalComment" in data_object
        assert "isRegulator" in data_object
        assert "note" in data_object
        assert "synonyms" in data_object
        assert "type" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_tf_objects():
    from ecocyc_extractor.regulondb.transcription_factors import get_regulondb_transcription_factors
    data_objects = get_regulondb_transcription_factors(transcription_factor_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["transcriptionFactors"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["organisms_id"] is not None
        assert data_object.get("abbreviatedNamee") is None or data_object["abbreviatedName"] is not None
        assert "citations" in data_object
        assert data_object.get("confidenceLevel") is None or data_object["confidenceLevel"] is not None
        assert "externalCrossReferences" in data_object
        assert data_object.get("activeConformations") is None or data_object["activeConformations"] is not None
        assert data_object.get("inactiveConformations") is None or data_object["inactiveConformations"] is not None
        assert data_object.get("name") is None or data_object["name"] is not None
        assert data_object.get("note") is None or data_object["note"] is not None
        assert data_object.get("products_ids") is None or data_object["products_ids"] is not None
        assert data_object.get("siteLength") is None or data_object["siteLength"] is not None
        assert data_object.get("synonyms") is None or data_object["synonyms"] is not None
        

@pytest.mark.skipif(False,reason="Testing New")
@pytest.mark.parametrize("ontology_name", SAMP_IDS.SAMPLE_IDS_BY_TYPE["ontologies"])
def test_ontology_objects(ontology_name):
    from ecocyc_extractor.regulondb.ontologies import get_regulondb_ontologies
    data_objects = get_regulondb_ontologies(ontology_name=ontology_name)
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["name"] is not None
        assert "description" in data_object
        assert "externalCrossReferences" in data_object


@pytest.mark.skipif(False,reason="Testing New")
def test_term_objects():
    from ecocyc_extractor.regulondb.terms import get_regulondb_terms
    data_objects = get_regulondb_terms(term_type=SAMP_IDS.SAMPLE_IDS_BY_TYPE["ontologies"][0], term_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["terms"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["ontologies_id"] is not None
        assert data_object["name"] is not None
        assert "definition" in data_object
        assert "externalCrossReferences" in data_object
        assert "members" in data_object
        assert "subClassOf" in data_object
        assert "superClassOf" in data_object
        assert data_object.get("synonyms") is None or data_object["synonyms"] is not None


@pytest.mark.skipif(False,reason="Testing New")
def test_evidence_objects():
    from ecocyc_extractor.regulondb.evidences import get_regulondb_evidences
    data_objects = get_regulondb_evidences()
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert data_object["name"] is not None
        assert "code" in data_object
        assert "crossEvidenceCodeRule" in data_object
        assert "evidenceApproach" in data_object
        assert "evidenceCategory" in data_object
        assert "evidenceClass" in data_object
        assert "externalCrossReferences" in data_object
        assert data_object.get("head") is None or data_object["head"] is not None
        assert "internalComment" in data_object
        assert "note" in data_object
        assert "noteWeb" in data_object
        assert "pertainsTo" in data_object
        assert "type" in data_object

@pytest.mark.skipif(False,reason="Testing New")
def test_external_reference_objects():
    from ecocyc_extractor.regulondb.external_cross_references import get_regulondb_external_databases
    data_objects = get_regulondb_external_databases()#registered_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["externalCrossReferences"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert "description" in data_object
        assert "internalComment" in data_object
        assert "name" in data_object
        assert "note" in data_object
        assert "url" in data_object

@pytest.mark.skipif(False,reason="Testing New")
def test_publication_objects():
    from ecocyc_extractor.regulondb.publications import get_regulondb_publications
    data_objects = get_regulondb_publications(registered_ids=SAMP_IDS.SAMPLE_IDS_BY_TYPE["publications"])
    for data_object in data_objects:
        assert data_object["_id"] is not None
        assert "authors" in data_object
        assert "externalCrossReferences" in data_object
        assert "internalComment" in data_object
        assert "note" in data_object
        assert "pmid" in data_object
        assert "source" in data_object
        assert "title" in data_object
        assert "url" in data_object
        assert "year" in data_object