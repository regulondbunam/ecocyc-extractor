def get_regulondb_ontologies(only_properties_with_values=False, ontology_name="multifun"):
    from ecocyc.collections.ontologies import Ontologies

    ontologies = Ontologies(ontology_name)

    for ontology in ontologies.objects:
        ontology_object = {
            "_id": ontology.id,
            "description": ontology.comment,
            "externalCrossReferences": ontology.db_links,
            "name": ontology.name,
        }
        if only_properties_with_values is True:
            ontology_object = ontology.get_only_properties_with_values(ontology_object)
        yield ontology_object
