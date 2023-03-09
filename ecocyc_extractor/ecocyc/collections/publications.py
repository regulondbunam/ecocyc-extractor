import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.publication import Publication


class Publications(object):

    pt_connection = Connection()

    def __init__(self, registered_ids=False):
        # print(registered_ids)
        self.ids = Publications.get_ids(registered_ids)

    @staticmethod
    def get_ids(registered_ids=False):
        if registered_ids:
            publication_ids = utils.get_publication_ids()
            print('Using local publications: ',
                  len(utils.get_publication_ids()))
        else:
            publication_ids = Publications.pt_connection.get_class_all_instances(
                EC.PUBLICATIONS_CLASS)
            print('Using all publications: ', len(publication_ids))
        return publication_ids

    @property
    def objects(self):
        publication_objects = Publications.pt_connection.get_frame_objects(
            self.ids)
        for publication in publication_objects:
            publication = Publications.set_publication(publication)
            logging.info(
                'Working on publication: {}'.format(publication["id"]))
            ecocyc_publication = Publication(**publication)
            yield ecocyc_publication

    @staticmethod
    def set_publication(publication):
        new_publication = dict(
            id=publication[EC.ID],
            authors=publication[EC.AUTHORS],
            comment=publication[EC.COMMENT],
            dblinks=publication[EC.DBLINKS],
            internal_comment=publication[EC.INTERNAL_COMMENT],
            medline_id=publication[EC.MEDLINE_ID],
            pubmed_id=publication[EC.PUBMED_ID],
            source=publication[EC.SOURCE],
            title=publication[EC.TITLE],
            url=publication[EC.URL],
            year=publication[EC.YEAR]
        )
        return new_publication
