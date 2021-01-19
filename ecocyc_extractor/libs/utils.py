import os
import logging
import json

def set_log(log_path):
    if not os.path.isdir(log_path):
        raise IOError("{} directory does not exist, please edit your log argument value".format(log_path))
    logging.basicConfig(filename=os.path.join(log_path, 'ecocyc_extractor.log'),
                        format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)


def validate_directories(output_path):
    # verifying that the output_path directory exists
    if not os.path.isdir(output_path):
        raise IOError(
            "{} directory does not exist, please "
            "check your --output argument value".format(
                output_path)
        )


def create_json(objects, filename, output):
    filename = os.path.join(output, filename)
    with open("{}.json".format(filename), 'w') as json_file:
        json.dump(objects, json_file, indent=2, sort_keys=True)