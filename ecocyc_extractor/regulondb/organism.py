"""
Organisms
"""
# standard

# third party

# local


def get_regulondb_organisms(only_properties_with_values=False, organism_name='ECOLI'):
    from ecocyc_extractor.ecocyc.collections.organisms import Organisms

    organisms = Organisms(organism_name)

    for organism in organisms.objects:
        organism_object = {
            "_id": organism.id, # str
            "citations": organism.citations, # str
            "description": organism.comment,# str
            "externalCrossReferences": organism.db_links, # obj array
            "genome": organism.genom, # str
            "internalComment": organism.comment_internal, # str
            "name": organism.name, # str
            "pgdbAuthors": organism.pgdb_authors, # array
            "pgdbCopyright": organism.pgdb_copyright, # array
            "pgdbName": organism.pgdb_name, # str
            "strainName": organism.strain_name, # str
            "synonyms": organism.synonyms, # array str
            "url": organism.url # posiblemente PGDB-Footer-Citation
        }
        if only_properties_with_values is True:
            organism_object = organism.get_only_properties_with_values(organism_object)
        yield organism_object