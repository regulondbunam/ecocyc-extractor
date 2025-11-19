"""
Utility functions.
"""
# standard
import os
import logging
import json

# third party

# local


def set_json_object(file_name, objs_to_json, organism, class_acronym, subclass_acronym):
    """
    Sets the JSON output format of the collection.

    Args:
        file_name: String, the output file name.
        class_acronym: String, the subclass acronym.
        subclass_acronym: String, the class child acronym.
        objs_to_json: List, the list with the collection data.
        organism: String, the organism name.

    Returns:
        objs_to_json: Dict, the dictionary with the final JSON file format
    """
    if "terms" in file_name or "ontologies" in file_name:
        if "multifun" in file_name:
            ontology_name = "multifun"

        elif "got" in file_name:
            ontology_name = "geneOntology"

        else:
            raise KeyError("ontology not implemented")

        collection_name = "terms" if "term" in file_name else "ontologies"
        objs_to_json = {
            "collectionName": collection_name,
            "collectionData": objs_to_json,
            "ontologyName": ontology_name,
            "subClassAcronym": subclass_acronym,
            "classAcronym": class_acronym
        }
        return objs_to_json
    else:
        objs_to_json = {
            "collectionName": file_name,
            "collectionData": objs_to_json,
            "organism": organism,
            "subClassAcronym": subclass_acronym,
            "classAcronym": class_acronym
        }
        return objs_to_json


def set_log(log_path, release_version, test):
    """
    Initializes the execution log to examine any problems that arise during extraction.

    Args:
        log_path: String, the path to the log file.
        release_version: String, the Ecocyc release version.
        test: Bool, flag for set log name in test mode.
    """
    if not os.path.isdir(log_path):
        raise IOError("{} directory does not exist, please edit your log argument value".format(log_path))
    file_name = f'ecocyc_extractor_release_{release_version}'
    if test:
        file_name = f'ecocyc_extractor_test_{release_version}'
    logging.basicConfig(filename=os.path.join(log_path, f'{file_name}.log'),
                        format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)


def validate_directories(output_path):
    """
    Validates the output directory exists, rise errors if it doesn't.

    Args:
        output_path: String, the path to the output directory.
    """
    if not os.path.isdir(output_path):
        raise IOError(
            f"{output_path} directory does not exist, please "
            "check your --output argument value"
        )


def create_json(objects, filename, output):
    """
    Create and write the JSON file with the results.

    Args:
        objects: Object, a Python serializable object that you want to convert to JSON format.
        filename: String, JSON file name.
        output: String, output path.
    """
    filename = os.path.join(output, filename)
    with open("{}.json".format(filename), 'w') as json_file:
        json.dump(objects, json_file, indent=2, sort_keys=True)
