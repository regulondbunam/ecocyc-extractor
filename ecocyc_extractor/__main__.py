from libs import utils
from libs import arguments
from regulondb import ontologies
from regulondb import terms
from regulondb import regulatory_continuants
from regulondb import regulatory_complexes
from regulondb import transcription_factor_regulatory_sites
from regulondb import regulatory_interactions
from regulondb import transcription_factors
from regulondb import sigma_factors
from regulondb import promoters
from regulondb import cryptic_prophages
from regulondb import terminators
from regulondb import operons
from regulondb import transcription_units
from regulondb import motifs
from regulondb import products
from regulondb import genes
from regulondb import external_cross_references
from regulondb import evidences
from regulondb import publications
from collections import OrderedDict
import sys
import os
sys.path.insert(0, os.path.abspath('.'))


def set_json_object(filename, objects_to_json, organism, class_acronym, subclass_acronym):
    if "terms" in filename or "ontologies" in filename:
        if "multifun" in filename:
            ontologyName = "multifun"

        elif "got" in filename:
            ontologyName = "geneOntology"

        else:
            raise KeyError("ontology not implemented")

        collection_name = "terms" if "term" in filename else "ontologies"
        objects_to_json = {
            "collectionName": collection_name,
            "collectionData": objects_to_json,
            "ontologyName": ontologyName,
            "subClassAcronym": subclass_acronym,
            "classAcronym": class_acronym
        }
        return objects_to_json
    else:
        objects_to_json = {
            "collectionName": filename,
            "collectionData": objects_to_json,
            "organism": organism,
            "subClassAcronym": subclass_acronym,
            "classAcronym": class_acronym
        }
        return objects_to_json


if __name__ == '__main__':
    arguments = arguments.load_arguments()

    # organism usage can be seen in the utils.constants module and on the
    # utils.pathway_tools.connection module
    organism = arguments.organism.upper()
    # So far the class acronym is the same as the organism name
    # unless something else is indicated, if so, it will be needed to be
    # implemented
    class_acronym = organism

    os.environ["ORGANISM"] = organism

    output_path = arguments.output
    utils.set_log(arguments.log)

    utils.validate_directories(output_path)

    files = OrderedDict()

    if arguments.all or arguments.genes:
        print("Setting up Genes' process")
        files["genes"] = genes.get_regulondb_genes(
            only_properties_with_values=True), organism, class_acronym, "GNC"
    if arguments.all or arguments.products:
        print("Setting up Products' process")
        files["products"] = products.get_regulondb_products(
            only_properties_with_values=True), organism, class_acronym, "PDC"
    if arguments.all or arguments.motifs:
        print("Setting up Motifs' process")
        files["motifs"] = motifs.get_regulondb_motifs(
            only_properties_with_values=True), organism, class_acronym, "MTC"

    if arguments.all or arguments.transcription_units:
        print("Setting up Transcription Units' process")
        files["transcriptionUnits"] = transcription_units.get_regulondb_transcription_units(
            only_properties_with_values=True), organism, class_acronym, "TUC"
    if arguments.all or arguments.operons:
        print("Setting up Operons' process")
        files["operons"] = operons.get_regulondb_operons(
            only_properties_with_values=True), organism, class_acronym, "OPC"

    if arguments.all or arguments.terminators:
        print("Setting up Terminators' process")
        files["terminators"] = terminators.get_regulondb_terminators(
            only_properties_with_values=True), organism, class_acronym, "TMC"

    if arguments.all or arguments.prophages:
        print("Setting up Cryptic Prophages' process")
        files["prophages"] = cryptic_prophages.get_regulondb_cryptic_prophages(
            only_properties_with_values=True), organism, class_acronym, "CPC"

    if arguments.all or arguments.promoters:
        print("Setting up Promoters' process")
        files["promoters"] = promoters.get_regulondb_promoters(
            only_properties_with_values=True), organism, class_acronym, "PMC"
    if arguments.all or arguments.sigma_factors:
        print("Setting up Sigma Factors' process")
        files["sigmaFactors"] = sigma_factors.get_regulondb_sigma_factors(
            only_properties_with_values=True), organism, class_acronym, "SFC"

    if arguments.all or arguments.regulatory_interactions:
        print("Setting up Regulatory Interactions' process")
        files["regulatoryInteractions"] = regulatory_interactions.get_regulondb_regulatory_interactions(
            only_properties_with_values=True),
        organism, class_acronym, "RIC"
    if arguments.all or arguments.sites:
        print("Setting up Sites' process")
        files["transcriptionFactorRegulatorySites"] = transcription_factor_regulatory_sites.get_regulondb_transcription_factor_regulatory_sites(
            only_properties_with_values=True), organism, class_acronym, "BSC"
    if arguments.all or arguments.regulatory_complexes:
        print("Setting up Regulatory Complexes' process")
        files["regulatoryComplexes"] = regulatory_complexes.get_regulondb_regulatory_complexes(
            only_properties_with_values=True, include_inactive=True), organism, class_acronym, "RCC"
    if arguments.all or arguments.regulatory_continuants:
        print("Setting up Regulatory Continuants' process")
        files["regulatoryContinuants"] = regulatory_continuants.get_regulondb_regulatory_continuants(
            only_properties_with_values=True), organism, class_acronym, "CNC"
    if arguments.all or arguments.transcription_factors:
        print("Setting up Transcription Factors' process")
        files["transcriptionFactors"] = transcription_factors.get_regulondb_transcription_factors(
            only_properties_with_values=True), organism, class_acronym, "TFC"

    if arguments.all or arguments.got_ontology:
        print("Setting up Ontologies' process")
        files["got_ontologies"] = ontologies.get_regulondb_ontologies(
            only_properties_with_values=True, ontology_name="gene-ontology"), organism, "ONTOL", "GON"
    if arguments.all or arguments.got_terms:
        print("Setting up Gene Ontology Terms' process")
        files["got_terms"] = terms.get_regulondb_terms(
            only_properties_with_values=True, term_type="gene-ontology"), organism, "ONTOL", "GON"
    if arguments.all or arguments.multifun_ontology:
        print("Setting up Ontologies' process")
        files["multifun_ontologies"] = ontologies.get_regulondb_ontologies(
            only_properties_with_values=True, ontology_name="multifun"), organism, "ONTOL", "MTF"
    if arguments.all or arguments.multifun_terms:
        print("Setting up Multifun Terms' process")
        files["multifun_terms"] = terms.get_regulondb_terms(
            only_properties_with_values=True, term_type="multifun"), organism, "ONTOL", "MTF"

    if arguments.all or arguments.evidences:
        print("Setting up Evidences' process")
        files["evidences"] = evidences.get_regulondb_evidences(
            only_properties_with_values=True), organism, class_acronym, "EVC"
    if arguments.all or arguments.external_databases or arguments.all_external_databases:
        print("Setting up External DBs' process")
        files["externalCrossReferences"] = external_cross_references.get_regulondb_external_databases(
            registered_ids=not arguments.all_external_databases, only_properties_with_values=True), organism, class_acronym, "ERC"
    if arguments.all or arguments.publications or arguments.all_publications:
        print("Setting up Publications' process")
        files["publications"] = publications.get_regulondb_publications(
            registered_ids=not arguments.all_publications, only_properties_with_values=True), organism, class_acronym, "PRC"

    for filename, (objects, organism, class_acronym, subclass_acronym) in files.items():
        print("Writing {} json file,".format(filename))
        objects_to_json = []
        for regulondb_object in objects:
            objects_to_json.append(regulondb_object.copy())

        print("\t total of {} objects: {}".format(
            filename, len(objects_to_json)))

        objects_to_json = set_json_object(
            filename, objects_to_json, organism, class_acronym, subclass_acronym)

        utils.create_json(objects_to_json, filename, output_path)
    print("Files created at {}".format(output_path))
