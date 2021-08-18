import logging

from ecocyc.utils.pathway_tools.connection import Connection
from ecocyc.utils import constants as EC, utils
from ecocyc.domain.regulatory_continuant import RegulatoryContinuant
from ecocyc.collections.regulatory_complexes import RegulatoryComplexes


class RegulatoryContinuants(object):

    pt_connection = Connection()
    regulatory_complexes = RegulatoryComplexes(include_inactive=True)

    def __init__(self, regulatory_complexes_compounds=True):
        self.ids = RegulatoryContinuants.get_ids(regulatory_complexes_compounds)

    @staticmethod
    def get_ids(regulatory_complexes_compounds=True):
        regulatory_continuant_ids = []
        if regulatory_complexes_compounds is True:
            for regulatory_complex_object in RegulatoryContinuants.regulatory_complexes.objects:
                regulatory_complex_compound_ids = regulatory_complex_object.compounds
                if regulatory_complex_compound_ids:
                    regulatory_continuant_ids.extend(regulatory_complex_compound_ids)
        else:
            regulatory_continuant_ids = RegulatoryContinuants.pt_connection.get_class_all_instances(EC.COMPOUNDS_CLASS)
        regulatory_continuant_ids = utils.get_unique_elements(regulatory_continuant_ids)
        return regulatory_continuant_ids

    @property
    def objects(self):
        regulatory_continuant_objects = RegulatoryContinuants.pt_connection.get_frame_objects(self.ids)
        for regulatory_continuant in regulatory_continuant_objects:
            regulatory_continuant = RegulatoryContinuants.set_regulatory_continuant(regulatory_continuant)
            logging.info('Working on regulatory continuant: {}'.format(regulatory_continuant["id"]))
            ecocyc_regulatory_continuant = RegulatoryContinuant(**regulatory_continuant)
            yield ecocyc_regulatory_continuant

    @staticmethod
    def set_regulatory_continuant(regulatory_continuant):
        new_regulatory_continuant = dict(
            id=regulatory_continuant[EC.ID],
            citations=regulatory_continuant[EC.CITATIONS],
            comment=regulatory_continuant[EC.COMMENT],
            dblinks=regulatory_continuant[EC.DBLINKS],
            internal_comment=regulatory_continuant[EC.INTERNAL_COMMENT],
            name=regulatory_continuant[EC.NAME],
            organism=EC.ORGANISM_ID,
            regulates=regulatory_continuant[EC.REGULATES],
            synonyms=regulatory_continuant[EC.SYNONYMS]
        )
        return new_regulatory_continuant
