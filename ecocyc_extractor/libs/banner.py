import json

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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
Version: {regulondb_version}
RegulonDB Version: {regulondb_version}
Ecocyc Version: {ecocyc_version}
GitHub: https://github.com/regulondbunam/ecocyc-extractor
"""
def show_banner():
    print(banner)