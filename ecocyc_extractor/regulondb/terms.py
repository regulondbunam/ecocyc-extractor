def get_regulondb_terms(only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.terms import Terms
    terms = Terms()

    for term in terms.objects:
        term_object = {
            "_id": term.id,
            "definition": term.definition,
            "citations": term.citations,
            "externalCrossReferences": term.db_links,
            "has": term.children_ids,
            "isA": term.parents_ids,
            "members": term.members,
            "name": term.name,
            "ontology_id": term.ontology_id,
            "synonyms": term.synonyms
        }
        if only_properties_with_values is True:
            term_object = term.get_only_properties_with_values(term_object)
        yield term_object
