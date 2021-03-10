import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.transcription_factor_regulatory_site import TranscriptionFactorRegulatorySite
from ecocyc_extractor.ecocyc.collections.regulatory_interactions import RegulatoryInteractions


class TranscriptionFactorRegulatorySites(object):
    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = self.get_ids(ids)

    @staticmethod
    def get_ids(site_ids=None):
        if site_ids is None:
            site_ids = []
            ri_ids = RegulatoryInteractions.get_ids(
                transcription_factors_ris=False)

            for ri_id in ri_ids:
                ri_site_ids = TranscriptionFactorRegulatorySite.pt_connection.get_slot_values(
                    ri_id, EC.ASSOCIATED_BINDING_SITE_SLOT)
                site_ids.extend(ri_site_ids)
            site_ids = utils.get_unique_elements(site_ids)
        site_ids = utils.get_unique_elements(site_ids)
        return site_ids

    @property
    def objects(self):
        site_objects = TranscriptionFactorRegulatorySite.pt_connection.get_frame_objects(
            self.ids)
        for site in site_objects:
            site = TranscriptionFactorRegulatorySites.set_site(site)
            logging.info('Working on site: {}'.format(site["id"]))
            ecocyc_site = TranscriptionFactorRegulatorySite(**site)
            yield ecocyc_site

    @staticmethod
    def set_site(site):
        site = dict(
            id=site[EC.ID],
            absolute_position=site[EC.ABSOLUTE_CENTER_POSITION],
            citations=site[EC.CITATIONS],
            comment=site[EC.COMMENT],
            dblinks=site[EC.DBLINKS],
            internal_comment=site[EC.INTERNAL_COMMENT],
            involved_in_regulation=site[EC.INVOLVED_IN_REGULATION],
            mechanism=site[EC.MECHANISM],
            length=site[EC.DNA_FOOTPRINT_SIZE],
            lend=site[EC.LEND],
            rend=site[EC.REND],
            organism=EC.ORGANISM_ID,
        )
        return site
