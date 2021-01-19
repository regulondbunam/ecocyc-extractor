def get_regulondb_evidences(registered_ids=False, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.evidences import Evidences
    evidences = Evidences(registered_ids)

    for evidence in evidences.objects:
        evidence_object = {
            "_id": evidence.id,
            "code": evidence.codes,
            "internalComment": evidence.internal_comment,
            "name": evidence.name,
            "note": evidence.comment,
            "pertainsTo": evidence.pertains_to
        }
        if only_properties_with_values is True:
            evidence_object = evidence.get_only_properties_with_values(evidence_object)
        yield evidence_object
