def get_regulondb_growth_condition_phrase_catalogs(gcpc_ids=None, only_properties_with_values=False):
    from ecocyc.collections.growth_condition_phrase_catalogs import GrowthConditionPhraseCatalogs
    growth_condition_phrase_catalogs = GrowthConditionPhraseCatalogs(gcpc_ids)

    for growth_condition_phrase_catalog in growth_condition_phrase_catalogs.objects:
        gcpc_object = {
            "_id": growth_condition_phrase_catalog.id,
            "description": growth_condition_phrase_catalog.description,
            "name": growth_condition_phrase_catalog.name,
            "terms": growth_condition_phrase_catalog.terms
        }
        if only_properties_with_values is True:
            gcpc_object = growth_condition_phrase_catalog.get_only_properties_with_values(gcpc_object)
        yield gcpc_object
