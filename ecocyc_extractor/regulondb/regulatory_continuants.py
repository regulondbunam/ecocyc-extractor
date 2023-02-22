def get_regulondb_regulatory_continuants(regulatory_complexes_compounds=True, only_properties_with_values=False):
    from ecocyc.collections.regulatory_continuants import RegulatoryContinuants
    regulatory_continuants = RegulatoryContinuants(
        regulatory_complexes_compounds)

    for regulatory_continuant in regulatory_continuants.objects:
        regulatory_continuant_object = {
            "_id": regulatory_continuant.id,
            "citations": regulatory_continuant.citations,
            "confidenceLevel": regulatory_continuant.confidence_level,
            "externalCrossReferences": regulatory_continuant.db_links,
            "internalComment": regulatory_continuant.internal_comment,
            "isRegulator": regulatory_continuant.is_regulator,
            "name": regulatory_continuant.name,
            "note": regulatory_continuant.comment,
            "organisms_id": regulatory_continuant.organism,
            "synonyms": regulatory_continuant.synonyms,
            "type": regulatory_continuant.type_
        }
        if only_properties_with_values is True:
            regulatory_continuant_object = regulatory_continuant.get_only_properties_with_values(
                regulatory_continuant_object)
        yield regulatory_continuant_object
