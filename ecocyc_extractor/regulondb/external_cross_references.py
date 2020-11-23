def get_regulondb_external_databases(registered_ids=False, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.external_databases import ExternalDatabases
    external_databases = ExternalDatabases(registered_ids)

    for external_database in external_databases.objects:
        external_database_object = {
            "_id": external_database.id,
            "description": external_database.description,
            "internalComment": external_database.internal_comment,
            "name": external_database.name,
            "note": external_database.comment,
            "url": external_database.url
        }
        if only_properties_with_values is True:
            external_database_object = external_database.get_only_properties_with_values(external_database_object)
        yield external_database_object

