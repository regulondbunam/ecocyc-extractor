def get_regulondb_promoters(promoter_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.promoters import Promoters

    promoters = Promoters(promoter_ids)

    for promoter in promoters.objects:
        promoter_object = {
            "_id": promoter.id,
            "citations": promoter.citations,
            "bindsSigmaFactor": promoter.binding_sigma_factor,
            "boxes": promoter.get_promoter_boxes(),
            "distanceToGene": promoter.distance_to_gene,
            "externalCrossReferences": promoter.db_links,
            "internalComment": promoter.internal_comment,
            "name": promoter.name,
            "note": promoter.comment,
            "organisms_id": promoter.organism,
            "sequence": promoter.sequence,
            "score": promoter.score,
            "strand": promoter.strand,
            "synonyms": promoter.synonyms,
            "transcriptionStartSite": promoter.transcription_start_site,
        }
        if only_properties_with_values is True:
            promoter_object = promoter.get_only_properties_with_values(promoter_object)
        yield promoter_object
