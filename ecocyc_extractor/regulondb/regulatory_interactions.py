def get_regulondb_regulatory_interactions(regulatory_interaction_ids=None, only_properties_with_values=False):
    from ecocyc.collections.regulatory_interactions import RegulatoryInteractions
    regulatory_interactions = RegulatoryInteractions(
        regulatory_interaction_ids)

    for regulatory_interaction in regulatory_interactions.objects:
        regulatory_interaction_object = {
            "_id": regulatory_interaction.id,
            "accessoryProteins": regulatory_interaction.accessory_proteins,
            "relativeDistSitePromoter": regulatory_interaction.relative_dist_site_promoter,
            "citations": regulatory_interaction.citations,
            "confidenceLevel": regulatory_interaction.confidence_level,
            "externalCrossReferences": regulatory_interaction.db_links,
            "function": regulatory_interaction.function_,
            "internalComment": regulatory_interaction.internal_comment,
            "note": regulatory_interaction.comment,
            "mechanism": regulatory_interaction.mechanism,
            "organisms_id": regulatory_interaction.organism,
            "regulatedEntity": regulatory_interaction.regulated_entity,
            "regulationType": regulatory_interaction.regulation_type,
            "regulator": regulatory_interaction.regulator,
            "regulatorySites_id": regulatory_interaction.binding_site,
            "regulationClass": regulatory_interaction.regulation_class
        }
        if only_properties_with_values is True:
            regulatory_interaction_object = regulatory_interaction.get_only_properties_with_values(
                regulatory_interaction_object)
        if not regulatory_interaction_object.get('regulator'):
            continue
        yield regulatory_interaction_object
