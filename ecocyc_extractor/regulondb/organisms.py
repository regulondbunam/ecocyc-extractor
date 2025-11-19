"""
Organisms
"""
# standard

# third party

# local


def get_regulondb_organisms(only_properties_with_values=False, organism_name='ECOLI'):
    from ecocyc.collections.organisms import Organisms

    organisms = Organisms(organism_name)

    for organism in organisms.objects:
        organism_object = {
            "_id": organism.id,
            "citations": organism.citations,
            "description": organism.comment,
            # "externalCrossReferences": organism.db_links,
            "genome": organism.genome,
            "internalComment": organism.comment_internal,
            "name": organism.name,
            "pgdbAuthors": organism.pgdb_authors,
            "pgdbCopyright": organism.pgdb_copyright,
            "pgdbName": organism.pgdb_name,
            "strainName": organism.strain_name,
            "synonyms": organism.synonyms,
            "url": organism.url
        }
        if only_properties_with_values is True:
            organism_object = organism.get_only_properties_with_values(organism_object)
        yield organism_object