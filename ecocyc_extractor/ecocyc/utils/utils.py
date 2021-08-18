import re

from .pathway_tools.connection import Connection
from .growth_conditions import GrowthCondition

pt_connection = Connection()
_publication_ids = []
_evidence_ids = []
_external_db_ids = []
pattern = "(GCs_GeneExpression_EXP:.+)\s*(GCs_GeneExpression_CONTROL:.+)\s*(<a href.*<\/a>)*"
pattern_2 = r"(Growth Condition-chip-Experiment:.+)\s*(Growth Conditions_GeneExpression_CONTROL:.+)\s*(<a href.*<\/a>)*"
citations_pattern = re.compile("(\[[0-9]+\])")


def add_pmids_to_extraction_from(comment):
    citations_pattern = re.compile("(\[[0-9]+\])")
    pmids_search = re.findall(citations_pattern, comment)
    pmids_search = list(set(pmids_search))
    for pmid in pmids_search:
        pmid = pmid[1:-1]
        if pmid.isdigit():
            get_citation_elements(pmid)


def get_unique_elements(elements):
    if isinstance(elements, (list, tuple)):
        elements = list(set(elements))
        elements = sorted(elements)
    return elements


def get_citation_elements(citation):
    evidence_id = None
    reference_id = None
    publication_id = None
    # This means that it has no evidence and  reference_id
    if citation == "":
        pass
    elif citation.isdigit():
        reference_id = citation
    # If the citation has an evidence_id but not a reference_i
    elif citation.startswith(":EV"):
        citation = citation.split(":")
        evidence_id = citation[1]
        evidence_id = "|{}|".format(evidence_id)
    # If the citation is only a reference_id and also has no other information
    elif citation.startswith("::") or citation.startswith(":::"):
        pass
    # If none of the previous conditionals are true then its a "valid" citation format
    else:
        citation = citation.replace("\\", "")
        evidence_id = pt_connection.citation_evidence_code(citation)
        reference_id = pt_connection.citation_id(citation)

    if evidence_id is not None:
        evidence_id = evidence_id.upper()
        if (pt_connection.is_an_instance_name(evidence_id) or pt_connection.is_a_class_name(evidence_id)) is False:
            evidence_id = None
        else:
            _evidence_ids.append(evidence_id)

    if reference_id is not None:
        reference_id = reference_id.upper()
        publication_id = "|PUB-{}|".format(reference_id)
        if (pt_connection.is_an_instance_name(publication_id) or pt_connection.is_a_class_name(publication_id)) is False:
            publication_id = None
        else:
            _publication_ids.append(publication_id)

    return evidence_id, publication_id


def get_citations(citations):
    try:
        object_citations = []
        for citation in sorted(citations):
            citation = citation.replace('"', "").replace(
                "[", "").replace("]", "").replace(" ", "").replace(",", "")
            citation = citation.strip()
            evidence_id, publication_id = get_citation_elements(citation)

            citation_object = {}

            if evidence_id is not None:
                citation_object['evidences_id'] = evidence_id

            if publication_id is not None:
                citation_object['publications_id'] = publication_id

            if citation_object and citation_object not in object_citations:
                object_citations.append(citation_object.copy())

        if not object_citations:
            object_citations = None

    except TypeError:
        object_citations = None
    return object_citations


def get_external_cross_references(dblinks):
    try:

        external_cross_references = []
        for database, records in dblinks.items():

            if (pt_connection.is_an_instance_name(database) or pt_connection.is_a_class_name(database)) is False:
                continue

            if "|REGULONDB|" == database:
                continue

            if isinstance(records, list):
                record_id = records[0]
            else:
                record_id = records

            external_x_ref_object = {
                "externalCrossReferences_id": database,
                "objectId": record_id
            }

            if external_x_ref_object not in external_cross_references:
                external_cross_references.append(external_x_ref_object.copy())

            _external_db_ids.append(database)

        if not external_cross_references:
            external_cross_references = None

    except AttributeError:
        external_cross_references = None

    return external_cross_references


def get_publication_ids():
    return get_unique_elements(_publication_ids)


def get_evidence_ids():
    return get_unique_elements(_evidence_ids)


def get_external_databases_ids():
    # We add them manually since we are referencing them through the Gene Domain
    # and there are not registered in the gene by default
    # REFSEQ is required for the bnumber
    # ECOCYC is required to mapped in through the frame_id of the gene
    _external_db_ids.append("|REFSEQ|")
    _external_db_ids.append("|ECOCYC|")
    return get_unique_elements(_external_db_ids)


def get_citations2(growth_condition, gc_evidences, gc_pmids):
    pmids_found = re.findall(citations_pattern, growth_condition)
    pmids_found = list(set(pmids_found))
    gc_evidences.extend([])
    gc_pmids.extend(pmids_found)


def get_growth_condition_from_comment(comment):
    if not comment:
        return []
    growth_conditions = re.match(pattern, comment)
    if growth_conditions is None:
        growth_conditions = re.match(pattern_2, comment)
    if growth_conditions is None:
        return []

    growth_conditions_phrases = []

    if growth_conditions is not None:
        experiment_gc = growth_conditions.group(1)
        experiment_gc = experiment_gc.replace("GCs_GeneExpression_EXP: ", "")
        experiment_gc = experiment_gc.replace("Growth Condition-chip-Experiment: ", "")
        experiment_gc = experiment_gc.replace("| ", "|")
        # print(experiment_gc)
        experiment_gc = experiment_gc.replace("/", "|")
        growth_conditions_phrases.append(experiment_gc)
        # print(experiment_gc)
        '''experiment_gc_terms = None
        if '|' in experiment_gc and experiment_gc is not None:
            experiment_gc_terms = experiment_gc.split('|')
        if '/' in experiment_gc and experiment_gc is not None:
            experiment_gc_terms = experiment_gc.split('/')
        print(experiment_gc_terms)'''

        control_gcs = growth_conditions.group(2)
        control_gcs = control_gcs.replace("; Es", "; /Es")
        control_gcs = control_gcs.split("; /")
        for control_gc in control_gcs:
            control_gc = control_gc.replace("GCs_GeneExpression_CONTROL: ", "")
            control_gc = control_gc.replace("Growth Conditions_GeneExpression_CONTROL: ", "")
            control_gc = control_gc.lstrip("2")
            control_gc = control_gc.lstrip(":")
            control_gc = control_gc.lstrip()
            control_gc = control_gc.replace("| ", "|")
            # print(control_gc)
            control_gc = control_gc.replace("/", "|")
            growth_conditions_phrases.append(control_gc)
        # print(control_gc)
        '''control_gc_terms = None
        if '|' in control_gc and control_gc is not None:
            control_gc_terms = control_gc.split('|')
        if '/' in control_gc and control_gc is not None:
            control_gc_terms = control_gc.split('/')
        print(control_gc_terms)'''

    return growth_conditions_phrases


def transform_growth_conditions(growth_conditions):
    transformed_gc = []
    if not growth_conditions:
        return None
    for growth_condition in growth_conditions:
        if "control" not in growth_condition.lower():
            continue
        growth_condition = growth_condition.replace("CONTROL2 ", "CONTROL:")
        growth_condition = growth_condition.replace("CONTROL: ", "CONTROL")
        growth_condition = growth_condition.replace("\n", "")
        growth_conditions = growth_condition.split('CONTROL')
        transformed_gc.extend(growth_conditions)
    return transformed_gc
