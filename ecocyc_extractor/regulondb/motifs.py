def get_regulondb_motifs(motif_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.motifs import Motifs
    motifs = Motifs(motif_ids)

    for motif in motifs.objects:
        motif_object = {
            "_id": motif.id,
            "alternateSequence": motif.alternate_sequence,
            "attachedGroup": motif.attached_group,
            "class": motif.class_,
            "color": motif.feature_color,
            "dataSource": motif.data_source,
            "description": motif.description,
            "externalCrossReferences": motif.db_links,
            "homologyMotif": motif.homology_motif,
            "internalComment": motif.internal_comment,
            "leftEndPosition": motif.left_end_position,
            "note": motif.comment,
            "organism_id": motif.organism,
            "product_id": motif.product_id,
            "rightEndPosition": motif.right_end_position,
            "sequence": motif.sequence,
            "residueNumber": motif.residue_number,
            "synonyms": motif.synonyms
        }
        if only_properties_with_values is True:
            motif_object = motif.get_only_properties_with_values(motif_object)
        yield motif_object

