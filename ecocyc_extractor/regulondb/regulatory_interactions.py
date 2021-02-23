def get_regulondb_regulatory_interactions(regulatory_interaction_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.regulatory_interactions import RegulatoryInteractions
    regulatory_interactions = RegulatoryInteractions(
        regulatory_interaction_ids)

    for regulatory_interaction in regulatory_interactions.objects:
        regulatory_interaction_object = {
            "_id": regulatory_interaction.id,
            "absoluteCenterPosition": regulatory_interaction.center_position,
            "citations": regulatory_interaction.citations,
            "externalCrossReferences": regulatory_interaction.db_links,
            "function": regulatory_interaction.function_,
            "internalComment": regulatory_interaction.internal_comment,
            "note": regulatory_interaction.comment,
            "organisms_id": regulatory_interaction.organism,
            "regulatedEntity": regulatory_interaction.regulated_entity,
            "regulator": regulatory_interaction.regulator,
            "transcriptionFactorRegulatorySites_id": regulatory_interaction.binding_site
        }
        if only_properties_with_values is True:
            regulatory_interaction_object = regulatory_interaction.get_only_properties_with_values(
                regulatory_interaction_object)
        yield regulatory_interaction_object
