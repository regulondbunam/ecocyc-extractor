"""
Connection module for ecocyc
"""
# standard

# third party
import pythoncyc
from pythoncyc import config as pconfig

# local
import ecocyc.utils.constants as EC


class Connection(object):
    _connection = None
    _organism_id = EC.ORGANISM_ID
    _cyc_host = EC.CYC_HOST
    _cyc_port = int(EC.CYC_PORT)

    def __new__(cls):
        if cls._connection is None:
            cls._connection = object.__new__(cls)
            cls._connection = Connection.set_pt_connection()
        return cls._connection

    @classmethod
    def set_pt_connection(cls):
        if cls._organism_id is None:
            raise EnvironmentError(
                'Environment variable "ORGANISM" has not been set, please provided one. File constants.py makes use of this.'
            )
        pconfig.set_host_name(cls._cyc_host)  # Remote PathwayTools host "192.168.0.17"
        pconfig.set_host_port(cls._cyc_port)  # Default Pathway Tools port 5008
        pathway_tools_connection = pythoncyc.select_organism(cls._organism_id)
        return pathway_tools_connection
