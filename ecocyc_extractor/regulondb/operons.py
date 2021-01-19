def get_regulondb_operons(only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.operons import Operons
    operons = Operons()

    for operon in operons.objects:
        operon_object = {
            "_id": operon.id,
            "name": operon.name,
            "organisms_id": operon.organism,
            "regulationPositions": operon.regulation_positions,
            "strand": operon.strand
        }
        if only_properties_with_values is True:
            operon_object = operon.get_only_properties_with_values(operon_object)
        yield operon_object
