"""
Banner module for ecocyc_extractor presentation.
"""
# standard
import json
import logging

# third party

# local

with open('config/config.json') as json_file:
    data = json.load(json_file)

print()

regulondb_version = data.get('version')
ecocyc_version = data.get('source_version')
extractor_version = data.get('extractor_version')

banner = f"""
REGULONDB's
███████╗ ██████╗ ██████╗  ██████╗██╗   ██╗ ██████╗    ███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗ ██████╗ ██████╗ 
██╔════╝██╔════╝██╔═══██╗██╔════╝╚██╗ ██╔╝██╔════╝    ██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
█████╗  ██║     ██║   ██║██║      ╚████╔╝ ██║         █████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ██║   ██║██████╔╝
██╔══╝  ██║     ██║   ██║██║       ╚██╔╝  ██║         ██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ██║   ██║██╔══██╗
███████╗╚██████╗╚██████╔╝╚██████╗   ██║   ╚██████╗    ███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║
╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
Version: {extractor_version}
RegulonDB Version: {regulondb_version}
Ecocyc Version: {ecocyc_version}
GitHub: https://github.com/regulondbunam/ecocyc-extractor
"""


def show_banner():
    """
    Prints the banner to the console and log.
    """
    print(banner)
    logging.info(banner)
