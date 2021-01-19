def get_regulondb_transcription_units(transcription_unit_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.transcription_units import TranscriptionUnits
    transcription_units = TranscriptionUnits(transcription_unit_ids)

    for transcription_unit in transcription_units.objects:
        transcription_unit_object = {
            "_id": transcription_unit.id,
            "citations": transcription_unit.citations,
            "externalCrossReferences": transcription_unit.db_links,
            "genes_ids": transcription_unit.gene_ids,
            "internalComment": transcription_unit.internal_comment,
            "name": transcription_unit.name,
            "note": transcription_unit.comment,
            "promoters_ids": transcription_unit.promoter_ids,
            "operons_id": transcription_unit.operon_id,
            "organisms_id": transcription_unit.organism,
            "terminators_ids": transcription_unit.terminator_ids,
            "synonyms": transcription_unit.synonyms
        }
        if only_properties_with_values is True:
            transcription_unit_object = transcription_unit.get_only_properties_with_values(transcription_unit_object)
        yield transcription_unit_object
