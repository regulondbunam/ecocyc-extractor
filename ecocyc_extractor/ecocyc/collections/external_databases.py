import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.external_database import ExternalDatabase


class ExternalDatabases(object):

    pt_connection = Connection()

    def __init__(self, registered_ids=False):
        self.ids = ExternalDatabases.get_ids(registered_ids)

    @staticmethod
    def get_ids(registered_ids=False):
        if registered_ids:
            external_db_ids = utils.get_external_databases_ids()
        else:
            external_db_ids = ExternalDatabases.pt_connection.get_class_all_instances(
                EC.EXTERNAL_DB_CLASS)
        return external_db_ids

    @property
    def objects(self):
        external_db_objects = ExternalDatabases.pt_connection.get_frame_objects(
            self.ids)
        for external_db in external_db_objects:
            external_db = ExternalDatabases.set_external_db(external_db)
            logging.info(
                'Working on external_db: {}'.format(external_db["id"]))
            ecocyc_external_db = ExternalDatabase(**external_db)
            yield ecocyc_external_db

    @staticmethod
    def set_external_db(external_db):
        new_external_db = dict(
            id=external_db[EC.ID],
            comment=external_db[EC.COMMENT],
            description=external_db[EC.NAME],
            internal_comment=external_db[EC.INTERNAL_COMMENT],
            name=external_db[EC.ID],
            url=external_db[EC.STATIC_SEARCH_URL]
        )
        return new_external_db
