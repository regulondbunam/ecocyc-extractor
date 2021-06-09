import logging

from ecocyc_extractor.ecocyc.utils.pathway_tools.connection import Connection
from ecocyc_extractor.ecocyc.utils import constants as EC, utils
from ecocyc_extractor.ecocyc.domain.segment import Segment


class Segments(object):

    pt_connection = Connection()

    def __init__(self, ids=None):
        self.ids = Segments.get_ids(ids)

    @staticmethod
    def get_ids(ids=None):
        if ids is None:
            dna_segments_ids = Segments.pt_connection.get_class_all_instances(EC.DNA_SEGMENTS)
            mrna_segments_ids = Segments.pt_connection.get_class_all_instances(EC.MRNA_SEGMENTS)
            segments_ids = dna_segments_ids + mrna_segments_ids
        else:
            segments_ids = ids
        segments_ids = utils.get_unique_elements(segments_ids)
        return segments_ids

    @property
    def objects(self):
        segments_objects = Segments.pt_connection.get_frame_objects(self.ids)
        for raw_segment in segments_objects:
            segment = Segments.set_segment(raw_segment)
            logging.info('Working on promoter: {}'.format(segment["id"]))
            ecocyc_segment = Segment(**segment)
            yield ecocyc_segment

    @staticmethod
    def set_segment(segment):
        new_segment = dict(
            id=segment[EC.ID],
            center_position=segment[EC.ABSOLUTE_CENTER_POSITION],
            citations=segment[EC.CITATIONS],
            dblinks=segment[EC.DBLINKS],
            name=segment[EC.NAME],
            lend=segment[EC.LEND],
            rend=segment[EC.REND],
            strand=segment[EC.TRANSCRIPTION_DIRECTION],
        )
        '''
        type=segment[EC.TYPE],
        parent=segment[EC.PARENT]
        '''
        return new_segment
