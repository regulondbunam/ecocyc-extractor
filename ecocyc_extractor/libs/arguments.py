import argparse


def argument_entities_provided(arguments):
    # This block of code is to see if the user has entities to process,
    # if not, then there's nothing to be downloaded so an error will be thrown,
    # finishing the execution.
    entities = vars(arguments)
    entities = dict(entities)
    entities["output"] = False
    entities["log"] = False
    entities["organism"] = False
    if not any(entities.values()):
        argparse.ArgumentError(
            "No objects' arguments provided. Use -h for help.")


def get_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="EcoCycExtractor",
        epilog="You need to provided at least one entity argument(--gene, --product, --promoter, etc...)",
    )

    parser.add_argument(
        "-a",
        "--all",
        help="Sets the extractor to download all the available classes, ignoring all arguments except --allpb and --alldb",
        action="store_true",
    )
    parser.add_argument(
        "-gn",
        "--genes",
        help="Sets the extractor to download Genes",
        action="store_true",
    )
    parser.add_argument(
        "-pd",
        "--products",
        help="Sets the extractor to download Products",
        action="store_true",
    )
    parser.add_argument(
        "-mt",
        "--motifs",
        help="Sets the extractor to download Motifs",
        action="store_true",
    )
    parser.add_argument(
        "-tu",
        "--transcription-units",
        help="Sets the extractor to download Transcription Units",
        action="store_true",
        dest="transcription_units",
    )
    parser.add_argument(
        "-op",
        "--operons",
        help="Sets the extractor to download Operons",
        action="store_true",
    )
    parser.add_argument(
        "-tm",
        "--terminators",
        help="Sets the extractor to download Terminators",
        action="store_true",
    )
    parser.add_argument(
        "-pm",
        "--promoters",
        help="Sets the extractor to download Promoters",
        action="store_true",
    )
    parser.add_argument(
        "-pph",
        "--prophages",
        help="Sets the extractor to download Cryptic Prophages",
        action="store_true",
        dest="prophages",
    )
    parser.add_argument(
        "-sg",
        "--segments",
        help="Sets the extractor to download Segments",
        action="store_true",
        dest="segments",
    )
    parser.add_argument(
        "-tf",
        "--transcription-factors",
        help="Sets the extractor to download Transcription Factors",
        action="store_true",
        dest="transcription_factors",
    )
    parser.add_argument(
        "-sf",
        "--sigma-factors",
        help="Sets the extractor to download Sigma Factors",
        action="store_true",
        dest="sigma_factors",
    )
    parser.add_argument(
        "-ri",
        "--regulatory-interactions",
        help="Sets the extractor to download Regulatory Interactions",
        action="store_true",
        dest="regulatory_interactions",
    )
    parser.add_argument(
        "-st",
        "--sites",
        help="Sets the extractor to download Sites",
        action="store_true",
    )
    parser.add_argument(
        "-rcplx",
        "--regulatory-complexes",
        help="Sets the extractor to download Regulatory Complexes",
        action="store_true",
        dest="regulatory_complexes",
    )
    parser.add_argument(
        "-rc",
        "--regulatory-continuants",
        help="Sets the extractor to download Regulatory Continuants",
        action="store_true",
        dest="regulatory_continuants",
    )
    parser.add_argument(
        "-ot",
        "--ontologies",
        help="Sets the extractor to download Ontologies(MultiFun, GO Terms)",
        action="store_true",
    )
    parser.add_argument(
        "-got",
        "--gene-ontology",
        help="Sets the extractor to download Ontologies(MultiFun, GO Terms)",
        action="store_true",
        dest="got_ontology",
    )
    parser.add_argument(
        "-gotm",
        "--got-terms",
        help="Sets the extractor to download Ontologies' Terms",
        action="store_true",
        dest="got_terms",
    )
    parser.add_argument(
        "-mot",
        "--multifun-ontology",
        help="Sets the extractor to download Ontologies(MultiFun, GO Terms)",
        action="store_true",
        dest="multifun_ontology",
    )
    parser.add_argument(
        "-mft",
        "--multifun-terms",
        help="Sets the extractor to download Ontologies' Terms",
        action="store_true",
        dest="multifun_terms",
    )

    parser.add_argument(
        "-ev",
        "--evidences",
        help="Sets the extractor to download Evidences",
        action="store_true",
    )
    parser.add_argument(
        "-extdb",
        "--external-databases",
        help="Sets the extractor to download External Databases",
        action="store_true",
    )
    parser.add_argument(
        "-pb",
        "--publications",
        help="Sets the extractor to download Publications",
        action="store_true",
    )
    parser.add_argument(
        "-allpb",
        "--all-publications",
        help="Sets the extractor to download all the Publications and not only the ones registered in the downloaded objects",
        action="store_true",
        dest="all_publications",
    )
    parser.add_argument(
        "-alldb",
        "--all-external-databases",
        help="Sets the extractor to download all the External Databases and not only the ones registered in the downloaded objects",
        action="store_true",
        dest="all_external_databases",
    )

    parser.add_argument(
        "-org",
        "--organism",
        help="Organism whose information is been downloaded",
        default="ECOLI",
        metavar="ecoli",
    )

    parser.add_argument(
        "-l",
        "--log",
        help="Path where the log of the process will be stored.",
        metavar="./Results/log",
        default="./Results/log",
    )

    parser.add_argument(
        "-out",
        "--output",
        help="Path where the json files of the process will be stored.",
        metavar="./Results/source/ecocyc",
        default="./Results/source/ecocyc",
    )
    arguments = parser.parse_args()
    return arguments


def load_arguments():

    arguments = get_arguments()

    argument_entities_provided(arguments)

    return arguments
