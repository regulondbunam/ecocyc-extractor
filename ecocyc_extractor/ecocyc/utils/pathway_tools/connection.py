import pythoncyc
import ecocyc_extractor.ecocyc.utils.constants as EC


class Connection(object):
    _connection = None
    _organism_id = EC.ORGANISM_ID

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
        pathway_tools_connection = pythoncyc.select_organism(cls._organism_id)
        return pathway_tools_connection
