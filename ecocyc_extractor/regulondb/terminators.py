def get_regulondb_terminators(terminator_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.terminators import Terminators
    terminators = Terminators(terminator_ids)

    for terminator in terminators.objects:
        terminator_object = {
            "_id": terminator.id,
            "class": terminator.class_,
            "citations": terminator.citations,
            "externalCrossReferences": terminator.db_links,
            "internalComment": terminator.internal_comment,
            "note": terminator.comment,
            "organism_id": terminator.organism,
            "sequence": terminator.sequence,
            "transcriptionTerminationSite": terminator.transcription_termination_site
        }
        if only_properties_with_values is True:
            terminator_object = terminator.get_only_properties_with_values(terminator_object)
        yield terminator_object
