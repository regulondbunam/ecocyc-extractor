def get_regulondb_terms(only_properties_with_values=False, term_type="gene-ontology"):
    from ecocyc.collections.terms import Terms
    terms = Terms(term_type)

    for term in terms.objects:
        term_object = {
            "_id": term.id,
            "definition": term.definition,
            "externalCrossReferences": term.db_links,
            "superClassOf": term.children_ids,
            "subClassOf": term.parents_ids,
            "members": term.members,
            "name": term.name,
            "ontologies_id": term.ontology_id,
            "synonyms": term.synonyms
        }
        if only_properties_with_values is True:
            term_object = term.get_only_properties_with_values(term_object)
        yield term_object
