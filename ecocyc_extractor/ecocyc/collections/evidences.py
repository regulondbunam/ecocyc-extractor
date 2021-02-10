import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.evidence import Evidence


class Evidences(object):

    pt_connection = Connection()

    def __init__(self, registered_ids=False):
        self.ids = Evidences.get_ids(registered_ids)

    @staticmethod
    def get_ids(registered_ids=False):
        if registered_ids:
            evidence_ids = utils.get_evidence_ids()
        else:
            evidence_ids = Evidences.pt_connection.get_class_all_subs(EC.EVIDENCE_CLASS)
        return evidence_ids

    @property
    def objects(self):
        evidence_objects = Evidences.pt_connection.get_frame_objects(self.ids)
        for evidence in evidence_objects:
            evidence = Evidences.set_evidence(evidence)
            logging.info("Working on evidence: {}".format(evidence["id"]))
            ecocyc_evidence = Evidence(**evidence)
            yield ecocyc_evidence

    @staticmethod
    def set_evidence(evidence):
        new_evidence = dict(
            id=evidence[EC.ID],
            code=evidence[EC.NAME],
            comment=evidence[EC.COMMENT],
            dblinks=evidence[EC.DBLINKS],
            externalCrossReferences=None,
            internal_comment=evidence[EC.INTERNAL_COMMENT],
            name=evidence[EC.NAME],
            pertains_to=evidence[EC.PERTAINS_TO],
        )
        return new_evidence
