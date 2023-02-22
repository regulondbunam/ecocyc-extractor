def get_regulondb_promoters(promoter_ids=None, only_properties_with_values=False):
    from ecocyc.collections.promoters import Promoters

    promoters = Promoters(promoter_ids)

    for promoter in promoters.objects:
        promoter_object = {
            "_id": promoter.id,
            "bindsSigmaFactor": promoter.binding_sigma_factor,
            "boxes": promoter.get_promoter_boxes(),
            "citations": promoter.citations,
            "confidenceLevel": promoter.confidence_level,
            "distanceToGene": promoter.distance_to_gene,
            "externalCrossReferences": promoter.db_links,
            "internalComment": promoter.internal_comment,
            "name": promoter.name,
            "note": promoter.comment,
            "organisms_id": promoter.organism,
            "score": promoter.score,
            "sequence": promoter.sequence,
            "strand": promoter.strand,
            "synonyms": promoter.synonyms,
            "transcriptionStartSite": promoter.transcription_start_site,
        }
        if only_properties_with_values is True:
            promoter_object = promoter.get_only_properties_with_values(
                promoter_object)
        yield promoter_object
