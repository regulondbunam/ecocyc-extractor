def get_regulondb_regulatory_complexes(regulatory_complex_ids=None, only_properties_with_values=False, include_inactive=False):
    from ecocyc_extractor.ecocyc.collections.regulatory_complexes import (RegulatoryComplexes)

    regulatory_complexes = RegulatoryComplexes(regulatory_complex_ids, include_inactive)

    for regulatory_complex in regulatory_complexes.objects:
        regulatory_complex_object = {
            "_id": regulatory_complex.id,
            "abbreviatedName": regulatory_complex.abbreviated_name,
            "externalCrossReferences": regulatory_complex.db_links,
            "internalComment": regulatory_complex.internal_comment,
            "name": regulatory_complex.name,
            "note": regulatory_complex.comment,
            "organisms_id": regulatory_complex.organism,
            "products": regulatory_complex.products,
            "regulatoryContinuants_ids": regulatory_complex.compounds,
            "synonyms": regulatory_complex.synonyms,
            "type": regulatory_complex.type_,
        }
        if only_properties_with_values is True:
            regulatory_complex_object = (regulatory_complex.get_only_properties_with_values(regulatory_complex_object))
        yield regulatory_complex_object
