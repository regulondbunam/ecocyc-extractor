def get_regulondb_sigma_factors(sigma_factor_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.sigma_factors import SigmaFactors
    sigma_factors = SigmaFactors(sigma_factor_ids)

    for sigma_factor in sigma_factors.objects:
        sigma_factor_object = {
            "_id": sigma_factor.id,
            "citations": sigma_factor.citations,
            "externalCrossReferences": sigma_factor.db_links,
            "gene_id": sigma_factor.gene,
            "internalComment": sigma_factor.internal_comment,
            "name": sigma_factor.name,
            "note": sigma_factor.comment,
            "organism_id": sigma_factor.organism,
            "synonyms": sigma_factor.synonyms,
        }
        if only_properties_with_values is True:
            sigma_factor_object = sigma_factor.get_only_properties_with_values(sigma_factor_object)
        yield sigma_factor_object