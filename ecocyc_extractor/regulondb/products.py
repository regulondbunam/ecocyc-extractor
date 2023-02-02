def get_regulondb_products(product_ids=None, only_properties_with_values=False):
    from ecocyc.collections.products import Products
    products = Products(product_ids)

    for product in products.objects:
        product_object = {
            "_id": product.id,
            "abbreviatedName": product.abbreviated_name,
            "anticodon": product.anticodon,
            "catalyzes": product.catalyzes,
            "codingSegments": product.coding_segments,
            "componentOf": product.component_of,
            "citations": product.citations,
            "consensusSequences": product.consensus_sequences,
            "externalCrossReferences": product.db_links,
            "genes_id": product.gene,
            "internalComment": product.internal_comment,
            "isoelectricPoints": product.isoelectric_points,
            "locations": product.locations,
            "modifiedForms": product.modified_forms,
            "molecularWeight": product.molecular_weight,
            "molecularWeightsKd": product.molecular_weights_kd,
            "name": product.name,
            "note": product.comment,
            "organisms_id": product.organism,
            "sequence": product.sequence,
            "siteLength": product.site_length,
            "spliceFormIntrons": product.splice_form_introns,
            "symmetries": product.symmetries,
            "synonyms": product.synonyms,
            "terms": product.terms,
            "type": product.type_
        }
        if only_properties_with_values is True:
            product_object = product.get_only_properties_with_values(product_object)
        yield product_object
