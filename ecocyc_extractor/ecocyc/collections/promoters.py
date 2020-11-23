import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.promoter import Promoter


class Promoters(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = self.get_ids(ids)

    @staticmethod
    def get_ids(ids=None):
        if ids is None:
            promoter_ids = Promoters.pt_connection.get_class_all_instances(EC.PROMOTER_CLASS)
        else:
            promoter_ids = ids
        promoter_ids = utils.get_unique_elements(promoter_ids)
        return promoter_ids

    @property
    def objects(self):
        promoter_objects = Promoters.pt_connection.get_frame_objects(self.ids)
        for raw_promoter in promoter_objects:
            promoters = Promoters.set_promoters(raw_promoter)
            for promoter in promoters:
                logging.info('Working on promoter: {}'.format(promoter["id"]))
                ecocyc_promoter = Promoter(**promoter)
                # If the promoter has more than one sigma factor then there's a special process. This special process
                # can be seen if the modified_id has a value and in the internal_comment content.
                # Afterwards we modify the id in order to reflect this special treatment.
                if ecocyc_promoter.modified_id:
                    ecocyc_promoter.id = ecocyc_promoter.modified_id
                yield ecocyc_promoter

    @staticmethod
    def set_promoters(promoter):
        sigma_factors_ids = Promoters.pt_connection.get_promoter_sigma_factor(promoter[EC.ID])
        sigma_factors_ids = utils.get_unique_elements(sigma_factors_ids)
        new_promoters = []
        new_promoter = dict(
            id=promoter[EC.ID],
            absolute_plus_1_pos=promoter[EC.ABSOLUTE_PLUS_1_POS],
            citations=promoter[EC.CITATIONS],
            comment=promoter[EC.COMMENT],
            dblinks=promoter[EC.DBLINKS],
            internal_comment=promoter[EC.INTERNAL_COMMENT],
            name=promoter[EC.NAME],
            offset=80,
            organism=EC.ORGANISM_ID,
            promoter_boxes=promoter[EC.PROMOTER_BOXES],
            strand=promoter[EC.TRANSCRIPTION_DIRECTION],
            synonyms=promoter[EC.SYNONYMS],
        )
        if sigma_factors_ids:
            new_promoters = Promoters.set_by_sigma_factors(new_promoter, sigma_factors_ids)
        else:
            new_promoters.append(new_promoter.copy())
        return new_promoters

    @staticmethod
    def set_by_sigma_factors(new_promoter, sigma_factor_ids):
        #TODO: To delete on Pathway Tools 24.5
        new_promoters = []
        if len(sigma_factor_ids) > 1:
            if new_promoter["internal_comment"] is None:
                new_promoter["internal_comment"] = []

            new_promoter["internal_comment"].append(
                ";[Modified-Promoter]; {} has more than 1 sigma factor, split into N promoters".format(
                    new_promoter["id"])
            )

            for sigma_factor_id in sigma_factor_ids:
                new_promoter.update(dict(modified_id="{};{}".format(new_promoter["id"], sigma_factor_id)))
                new_promoter.update(dict(sigma_factor=sigma_factor_id))
                new_promoters.append(new_promoter.copy())

        else:
            new_promoter.update(dict(sigma_factor=sigma_factor_ids[0]))
            new_promoters.append(new_promoter.copy())
        return new_promoters
