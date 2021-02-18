def get_regulondb_cryptic_prophages(cryptic_prophages_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.cryptic_prophages import CrypticProphages

    cryptic_prophages = CrypticProphages(cryptic_prophages_ids)

    for cryptic_prophage in cryptic_prophages.objects:
        cryptic_prophages_object = {
            "_id": cryptic_prophage.id,
            "citations": cryptic_prophage.citations,
            "externalCrossReferences": cryptic_prophage.db_links,
            "name": cryptic_prophage.name,
            "left_end_position": cryptic_prophage.left_end_position,
            "right_end_position": cryptic_prophage.right_end_position,
            "strand": cryptic_prophage.strand,
            "synonyms": cryptic_prophage.synonyms,
        }
        if only_properties_with_values is True:
            cryptic_prophages_object = cryptic_prophage.get_only_properties_with_values(
                cryptic_prophages_object)
        yield cryptic_prophages_object
