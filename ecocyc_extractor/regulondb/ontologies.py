def get_regulondb_ontologies(only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.ontologies import Ontologies
    ontologies = Ontologies()

    for ontology in ontologies.objects:
        ontology_object = {
            "_id": ontology.id,
            "description": ontology.comment,
            "name": ontology.name
        }
        if only_properties_with_values is True:
            ontology_object = ontology.get_only_properties_with_values(ontology_object)
        yield ontology_object

