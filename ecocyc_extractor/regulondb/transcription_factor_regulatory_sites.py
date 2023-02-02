def get_regulondb_transcription_factor_regulatory_sites(site_ids=None, only_properties_with_values=False):
    from ecocyc.collections.transcription_factor_regulatory_sites import TranscriptionFactorRegulatorySites

    TranscriptionFactorRegulatorySites = TranscriptionFactorRegulatorySites(
        site_ids)

    for site in TranscriptionFactorRegulatorySites.objects:
        site_object = {
            "_id": site.id,
            "absolutePosition": site.absolute_position,
            "citations": site.citations,
            "externalCrossReferences": site.db_links,
            "internalComment": site.internal_comment,
            "leftEndPosition": site.left_end_position,
            "length": site.length,
            "note": site.comment,
            "organisms_id": site.organism,
            "regulationType": site.regulation_type,
            "rightEndPosition": site.right_end_position,
            "sequence": site.sequence
        }
        if only_properties_with_values is True:
            site_object = site.get_only_properties_with_values(site_object)
        yield site_object
