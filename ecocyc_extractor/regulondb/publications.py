def get_regulondb_publications(registered_ids=False, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.publications import Publications

    publications = Publications(registered_ids)

    for publication in publications.objects:
        publication_object = {
            "_id": publication.id,
            "authors": publication.authors,
            "externalCrossReferences": publication.db_links,
            "internalComment": publication.internal_comment,
            "note": publication.comment,
            "pmid": publication.pmid,
            "source": publication.source,
            "title": publication.title,
            "url": publication.url,
            "year": publication.year,
        }
        if only_properties_with_values is True:
            publication_object = publication.get_only_properties_with_values(publication_object)
        yield publication_object
