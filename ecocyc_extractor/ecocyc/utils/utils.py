import re

from pathway_tools.connection import Connection

pt_connection = Connection()
_publication_ids = []
_evidence_ids = []
_external_db_ids = []


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
            citation = citation.replace('"', "").replace("[", "").replace("]", "").replace(" ", "").replace(",", "")
            citation = citation.strip()
            evidence_id, publication_id = get_citation_elements(citation)

            citation_object = {}

            if evidence_id is not None:
                citation_object['evidence_id'] = evidence_id

            if publication_id is not None:
                citation_object['publication_id'] = publication_id

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
        for database, records in dblinks.iteritems():

            if (pt_connection.is_an_instance_name(database) or pt_connection.is_a_class_name(database)) is False:
                continue

            if "|REGULONDB|" == database:
                continue

            if isinstance(records, list):
                record_id = records[0]
            else:
                record_id = records

            external_x_ref_object = {
                "externalCrossReference_id": database,
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
