import logging
from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.regulatory_interaction import RegulatoryInteraction


class RegulatoryInteractions(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = RegulatoryInteractions.get_ids(ids)

    @staticmethod
    def get_ids(ids=None, transcription_factors_ris=False):
        if ids is None and transcription_factors_ris is True:
            regulatory_interaction_ids = RegulatoryInteractions.pt_connection.get_class_all_instances(EC.TRANSCRIPTION_FACTOR_BINDING_CLASS)
            regulatory_interaction_ids.extend(RegulatoryInteractions.pt_connection.get_class_all_instances(EC.ALLOSTERIC_REGULATION_OF_RNAP))
        elif ids is None and transcription_factors_ris is False:
            regulatory_interaction_ids = RegulatoryInteractions.pt_connection.get_class_all_instances(EC.TRANSCRIPTION_FACTOR_BINDING_CLASS)
            regulatory_interaction_ids.extend(RegulatoryInteractions.pt_connection.get_class_all_instances(EC.ALLOSTERIC_REGULATION_OF_RNAP))
            #TODO: We need to add the new RIs from Soco's notes
        else:
            regulatory_interaction_ids = ids
        regulatory_interaction_ids = utils.get_unique_elements(regulatory_interaction_ids)
        return regulatory_interaction_ids

    @property
    def objects(self):
        regulatory_interaction_objects = RegulatoryInteractions.pt_connection.get_frame_objects(self.ids)
        for regulatory_interaction in regulatory_interaction_objects:
            regulatory_interaction = RegulatoryInteractions.set_regulatory_interaction(regulatory_interaction)
            logging.info('Working on regulatory interaction: {}'.format(regulatory_interaction["id"]))
            ecocyc_regulatory_interaction = RegulatoryInteraction(**regulatory_interaction)
            yield ecocyc_regulatory_interaction

    @staticmethod
    def set_regulatory_interaction(regulatory_interaction):
        new_regulatory_interaction = dict(
            id=regulatory_interaction[EC.ID],
            citations=regulatory_interaction[EC.CITATIONS],
            comment=regulatory_interaction[EC.COMMENT],
            dblinks=regulatory_interaction[EC.DBLINKS],
            internal_comment=regulatory_interaction[EC.INTERNAL_COMMENT],
            mode=regulatory_interaction[EC.MODE],
            organism=EC.ORGANISM_ID,
            regulated_entity=regulatory_interaction[EC.REGULATED_ENTITY],
            regulator=regulatory_interaction[EC.REGULATOR],
            site=regulatory_interaction[EC.ASSOCIATED_BINDING_SITE]
        )
        return new_regulatory_interaction

