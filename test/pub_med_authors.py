from Bio import Entrez, Medline


def get_pubmed_data(pmid, email='reguadm@ccg.unam.mx'):
    '''
    Connects to PUBMED database through Entrez API and gets the necessary publication data.
    The Entrez API returns a dictionary with the medline data, see also https://biopython.org/docs/1.75/api/Bio.Medline.html for more information about the keys obtained from this dictionary.

    Param
        pmid, Integer, PUBMED publication id.
        email, String, User email address to connect to PUBMED database.

    Returns
        publication, Dict, dictionary with the publication data.
    '''
    if not pmid:
        return None
    Entrez.email = email
    publications = []
    if isinstance(pmid, int) or isinstance(pmid, float):
        pmid = [pmid]
    elif isinstance(pmid, str):
        pmid = pmid.replace(' ', '')
        pmid = pmid.split(',')
    # for pmid in pmid:
    if isinstance(pmid, float):
        pmid = int(pmid)
    # print(pmid)
    handle = Entrez.efetch(db='pubmed', id=pmid,
                           rettype='medline', retmode='text')
    publication = {}
    record = Medline.read(handle)
    pubmed_authors = record.get('AU')
    print(record)
    if isinstance(pubmed_authors, str):
        pubmed_authors = pubmed_authors.split(',')
    publication.setdefault('authors', pubmed_authors)
    publication.setdefault('abstract', record.get('AB'))
    publication.setdefault('date', record.get('DP'))
    publication.setdefault('pmcid', record.get('PMC'))
    publication.setdefault('pmid', int(record.get('PMID')))
    publication.setdefault('title', record.get('TI'))
    article_identifier = record.get('AID')
    for identifier in article_identifier:
        if ' [doi]' in identifier:
            publication.setdefault(
                'doi', identifier.replace(' [doi]', ''))
    publication = {k: v for k, v in publication.items() if v}
    publications.append(publication)
    return publications


pmid = 12558182
pubmed_publication = get_pubmed_data(pmid=pmid)
print(pubmed_publication)
