def get_regulondb_segments(segments_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.segments import Segments

    segments = Segments(segments_ids)

    for segment in segments.objects:
        segments_object = {
            "_id": segment.id,
            "absoluteCenterPosition": segment.center_position,
            "citations": segment.citations,
            "externalCrossReferences": segment.db_links,
            "name": segment.name,
            "left_end_position": segment.left_end_position,
            "right_end_position": segment.right_end_position,
            "parentClass": segment.parent,
            "strand": segment.strand,
            "type": segment.segment_type,
        }
        if only_properties_with_values is True:
            segments_object = segment.get_only_properties_with_values(
                segments_object)
        yield segments_object
