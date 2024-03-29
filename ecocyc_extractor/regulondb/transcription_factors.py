def get_regulondb_transcription_factors(transcription_factor_ids=None, only_properties_with_values=False):
    from ecocyc.collections.transcription_factors import TranscriptionFactors
    transcription_factors = TranscriptionFactors(transcription_factor_ids)

    for transcription_factor in transcription_factors.objects:
        transcription_factor_rdb_object = {
            "_id": transcription_factor.id,
            "activeConformations": transcription_factor.active_conformations,
            "abbreviatedName": transcription_factor.abbreviated_name,
            "citations": transcription_factor.citations,
            "confidenceLevel": transcription_factor.confidence_level,
            "externalCrossReferences": transcription_factor.db_links,
            "globalFunction": transcription_factor.global_function,
            "inactiveConformations": transcription_factor.inactive_conformations,
            "name": transcription_factor.name,
            "note": transcription_factor.comment,
            "organisms_id": transcription_factor.organism,
            "products_ids": transcription_factor.get_products_ids(),
            "siteLength": transcription_factor.site_length,
            "synonyms": transcription_factor.synonyms,
            "symmetry": transcription_factor.symmetry
        }
        if only_properties_with_values is True:
            transcription_factor_rdb_object = transcription_factor.get_only_properties_with_values(
                transcription_factor_rdb_object)
        yield transcription_factor_rdb_object
