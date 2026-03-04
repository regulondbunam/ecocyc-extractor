import re

import pythoncyc
from pythoncyc import config as pconfig


pconfig.set_host_name("127.0.0.1")
pconfig.set_host_port(5008)

ORGANISM_ID = '|ECOLI|'
connection = pythoncyc.select_organism(ORGANISM_ID)

_publication_ids = []
_evidence_ids = []

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
        evidence_id = connection.citation_evidence_code(citation)
        reference_id = connection.citation_id(citation)

    if evidence_id is not None:
        evidence_id = evidence_id.upper()
        if (connection.is_an_instance_name(evidence_id) or connection.is_a_class_name(evidence_id)) is False:
            evidence_id = None
        else:
            _evidence_ids.append(evidence_id)

    if reference_id is not None:
        reference_id = reference_id.upper()
        publication_id = "|PUB-{}|".format(reference_id)
        if (connection.is_an_instance_name(publication_id) or connection.is_a_class_name(publication_id)) is False:
            publication_id = None
        else:
            _publication_ids.append(publication_id)

    return evidence_id, publication_id


biologic_entity_id = '|MICF-RNA|'
biologic_entity_obj = connection.get_frame_object(biologic_entity_id)

# print(biologic_entity_obj.keys())

comment = biologic_entity_obj.get('|COMMENT|')
# print(comment)
pub_pattern = re.compile(r"(\[[0-9]+\])")
# pub_pattern = re.compile(r"([0-9]+)")
found_pmids = list(set(re.findall(pub_pattern, comment[0])))
# [print(p) for p in found_pmids]
pub_ids = [f'|PUB-{int(id[1:-1])}|' for id in found_pmids]
# print(pub_ids)
[get_citation_elements(pmid[1:-1]) for pmid in found_pmids]

for pmid in pub_ids:
    print(pmid)
    pub_obj = connection.get_frame_object(pmid)
    # print(pub_obj.keys())
    # print(f'PMID: {pub_obj.get("|PUBMED-ID|")}', f'TITLE: {pub_obj.get("|TITLE|")}')

print(_publication_ids)

pmids_sample = [
 '|PUB-2436145|', '|PUB-2478539|', '|PUB-11029695|', '|PUB-1702997|',
 '|PUB-2439487|', '|PUB-7519595|', '|PUB-1715858|', '|PUB-11766055|',
 '|PUB-21398557|', '|PUB-7679383|', '|PUB-9139902|', '|PUB-2848006|',
 '|PUB-1510409|', '|PUB-7896685|', '|PUB-9343820|', '|PUB-11353631|',
 '|PUB-8234347|', '|PUB-22324810|', '|PUB-6201848|', '|PUB-7534474|',
 '|PUB-9478198|', '|PUB-8522136|', '|PUB-17264113|', '|PUB-14622403|',
 '|PUB-18388495|', '|PUB-3888961|', '|PUB-3007299|', '|PUB-2443485|',
 '|PUB-9063979|', '|PUB-1695892|', '|PUB-1723390|', '|PUB-7934849|',
 '|PUB-8034583|', '|PUB-7891555|', '|PUB-8002608|', '|PUB-8522515|',
 '|PUB-8825776|', '|PUB-8626315|', '|PUB-8655567|', '|PUB-8809747|',
 '|PUB-8899987|', '|PUB-9192630|', '|PUB-10398829|', '|PUB-10631293|',
 '|PUB-10802742|', '|PUB-10850996|', '|PUB-11073934|', '|PUB-11724537|',
 '|PUB-12713466|', '|PUB-15466019|', '|PUB-40694573|', '|PUB-2450678|',
 '|PUB-7689446|', '|PUB-7540245|', '|PUB-8809744|', '|PUB-9255788|',
 '|PUB-10068996|', '|PUB-11601842|', '|PUB-15063850|', '|PUB-15487940|',
 '|PUB-15466017|', '|PUB-16951250|', '|PUB-17055775|', '|PUB-17381274|',
 '|PUB-20068355|', '|PUB-22380658|', '|PUB-27404040|', '|PUB-29992897|'
]