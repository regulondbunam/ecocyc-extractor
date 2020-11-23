import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import json
import argparse
import logging
from collections import OrderedDict

from regulondb import publications
from regulondb import evidences
from regulondb import external_cross_references
from regulondb import genes
from regulondb import products
from regulondb import motifs
from regulondb import transcription_units
from regulondb import operons
from regulondb import terminators
from regulondb import promoters
from regulondb import sigma_factors
from regulondb import regulatory_interactions
from regulondb import regulatory_complexes
from regulondb import regulatory_continuants
from regulondb import terms
from regulondb import ontologies

import dotenv

dotenv.l

def create_json(objects, filename, output):
    filename = os.path.join(output, filename)
    with open("{}.json".format(filename), 'w') as json_file:
        json.dump(objects, json_file, indent=2, sort_keys=True)


def load_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="EcoCycExtractor", epilog="You need to provided at least one entity argument(--gene, --product, --promoter, etc...)")

    parser.add_argument(
        "-a", "--all",
        help="Sets the extractor to download all the available classes, ignoring all arguments except --allpb and --alldb",
        action='store_true'
    )
    parser.add_argument(
        "-gn", "--genes",
        help="Sets the extractor to download Genes",
        action='store_true'
    )
    parser.add_argument(
        "-pd", "--products",
        help="Sets the extractor to download Products",
        action='store_true'
    )
    parser.add_argument(
        "-mt", "--motifs",
        help="Sets the extractor to download Motifs",
        action='store_true'
    )
    parser.add_argument(
        "-tu", "--transcription-units",
        help="Sets the extractor to download Transcription Units",
        action='store_true',
        dest='transcription_units'
    )
    parser.add_argument(
        "-op", "--operons",
        help="Sets the extractor to download Operons",
        action='store_true'
    )
    parser.add_argument(
        "-tm", "--terminators",
        help="Sets the extractor to download Terminators",
        action='store_true'
    )
    parser.add_argument(
        "-pm", "--promoters",
        help="Sets the extractor to download Promoters",
        action='store_true'
    )
    parser.add_argument(
        "-sf", "--sigma-factors",
        help="Sets the extractor to download Sigma Factors",
        action='store_true',
        dest='sigma_factors'
    )
    parser.add_argument(
        "-ri", "--regulatory-interactions",
        help="Sets the extractor to download Regulatory Interactions",
        action='store_true',
        dest='regulatory_interactions'
    )
    parser.add_argument(
        "-rcplx", "--regulatory-complexes",
        help="Sets the extractor to download Regulatory Complexes",
        action='store_true',
        dest='regulatory_complexes'
    )
    parser.add_argument(
        "-rc", "--regulatory-continuants",
        help="Sets the extractor to download Regulatory Continuants",
        action='store_true',
        dest='regulatory_continuants'
    )
    parser.add_argument(
        "-ot", "--ontologies",
        help="Sets the extractor to download Ontologies(MultiFun, GO Terms)",
        action='store_true'
    )
    parser.add_argument(
        "-otm", "--terms",
        help="Sets the extractor to download Ontologies' Terms",
        action='store_true'
    )
    parser.add_argument(
        "-ev", "--evidences",
        help="Sets the extractor to download Evidences",
        action='store_true'
    )
    parser.add_argument(
        "-extdb", "--external-databases",
        help="Sets the extractor to download External Databases",
        action='store_true'
    )
    parser.add_argument(
        "-pb", "--publications",
        help="Sets the extractor to download Publications",
        action='store_true'
    )
    parser.add_argument(
        '-allpb', '--all-publications',
        help="Sets the extractor to download all the Publications and not only the ones registered in the downloaded objects",
        action='store_true',
        dest='all_publications'
    )
    parser.add_argument(
        '-alldb', '--all-external-databases',
        help="Sets the extractor to download all the External Databases and not only the ones registered in the downloaded objects",
        action='store_true',
        dest='all_external_databases'
    )

    parser.add_argument(
        "-org", "--organism",
        help="Organism whose information is been downloaded",
        default="ecoli",
        metavar="ecoli"
    )

    parser.add_argument(
        "-l", "--log",
        help="Path where the log of the process will be stored.",
        metavar="/Users/pablo/Proyectos/RegulonDB/Results/log",
        default="/Users/pablo/Proyectos/RegulonDB/Results/log"
    )

    parser.add_argument(
        "-out", "--output",
        help="Path where the json files of the process will be stored.",
        metavar="/Users/pablo/Proyectos/RegulonDB/Results/source/ecocyc",
        default="/Users/pablo/Proyectos/RegulonDB/Results/source/ecocyc"
    )
    arguments = parser.parse_args()
    return arguments


def argument_entities_provided(arguments):
    # This block of code is to see if the user has entities to process, if not, then there's nothing to be downloaded
    # so an error will be thrown, finishing the execution.
    entities = vars(arguments)
    entities = dict(entities)
    entities["output"] = False
    entities["log"] = False
    entities["organism"] = False
    if not any(entities.values()):
        argparse.ArgumentError("No objects' arguments provided. Use -h for help.")


def set_log(log_path):
    if not os.path.isdir(log_path):
        raise IOError("{} directory does not exist, please edit your log argument value".format(log_path))
    logging.basicConfig(filename=os.path.join(log_path, 'ecocyc_extractor.log'),
                        format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)


if __name__ == '__main__':
    arguments = load_arguments()
    argument_entities_provided(arguments)
    # organism usage can be seen in the utils.constants module and on the utils.pathway_tools.connection module
    os.environ["ORGANISM"] = arguments.organism

    output_path = arguments.output
    set_log(arguments.log)

    # verifying that the output_path directory exists
    if not os.path.isdir(output_path):
        raise IOError("{} directory does not exist, please check your --output argument value".format(output_path))

    files = OrderedDict()

    if arguments.all or arguments.genes:
        print "Setting up Genes' process"
        files["gene"] = genes.get_regulondb_genes(only_properties_with_values=True)
    if arguments.all or arguments.products:
        print "Setting up Products' process"
        files["product"] = products.get_regulondb_products(only_properties_with_values=True)
    if arguments.all or arguments.motifs:
        print "Setting up Motifs' process"
        files["motif"] = motifs.get_regulondb_motifs(only_properties_with_values=True)

    if arguments.all or arguments.transcription_units:
        print "Setting up Transcription Units' process"
        files["transcriptionUnit"] = transcription_units.get_regulondb_transcription_units(only_properties_with_values=True)
    if arguments.all or arguments.operons:
        print "Setting up Operons' process"
        files["operon"] = operons.get_regulondb_operons(only_properties_with_values=True)

    if arguments.all or arguments.terminators:
        print "Setting up Terminators' process"
        files["terminator"] = terminators.get_regulondb_terminators(only_properties_with_values=True)

    if arguments.all or arguments.promoters:
        print "Setting up Promoters' process"
        files["promoter"] = promoters.get_regulondb_promoters(only_properties_with_values=True)
    if arguments.all or arguments.sigma_factors:
        print "Setting up Sigma Factors' process"
        files["sigmaFactor"] = sigma_factors.get_regulondb_sigma_factors(only_properties_with_values=True)

    if arguments.all or arguments.regulatory_interactions:
        print "Setting up Regulatory Interactions' process"
        files["regulatoryInteraction"] = regulatory_interactions.get_regulondb_regulatory_interactions(only_properties_with_values=True)
    if arguments.all or arguments.regulatory_complexes:
        print "Setting up Regulatory Complexes' process"
        files["regulatoryComplex"] = regulatory_complexes.get_regulondb_regulatory_complexes(only_properties_with_values=True, include_inactive=True)
    if arguments.all or arguments.regulatory_continuants:
        print "Setting up Regulatory Continuants' process"
        files["regulatoryContinuant"] = regulatory_continuants.get_regulondb_regulatory_continuants(only_properties_with_values=True)

    if arguments.all or arguments.ontologies:
        print "Setting up Ontologies' process"
        files["ontology"] = ontologies.get_regulondb_ontologies(only_properties_with_values=True)
    if arguments.all or arguments.terms:
        print "Setting up Ontologies Terms' process"
        files["term"] = terms.get_regulondb_terms(only_properties_with_values=True)

    if arguments.all or arguments.evidences:
        print "Setting up Evidences' process"
        files["evidence"] = evidences.get_regulondb_evidences(only_properties_with_values=True)
    if arguments.all or arguments.external_databases or arguments.all_external_databases:
        print "Setting up External DBs' process"
        files["externalCrossReference"] = external_cross_references.get_regulondb_external_databases(registered_ids=not arguments.all_external_databases, only_properties_with_values=True)
    if arguments.all or arguments.publications or arguments.all_publications:
        print "Setting up Publications' process"
        files["publication"] = publications.get_regulondb_publications(registered_ids=not arguments.all_publications, only_properties_with_values=True)

    for file_name, objects in files.iteritems():
        print "Writing {} json file,".format(file_name)
        objects_to_json = []
        for regulondb_object in objects:
            objects_to_json.append(regulondb_object.copy())
        print "\t total of {} objects: {}".format(file_name, len(objects_to_json))
        objects_to_json = {
            file_name: objects_to_json
        }
        create_json(objects_to_json, file_name, output_path)
    print "Files created at {}".format(output_path)
