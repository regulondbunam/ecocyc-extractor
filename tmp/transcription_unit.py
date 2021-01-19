import pythoncyc

pt_connection = pythoncyc.select_organism('ecoli')

tu_ids = pt_connection.get_class_all_instances("|Transcription-Units|")

for tu_id in tu_ids:
    tu_components = pt_connection.get_slot_values(tu_id, "|COMPONENTS|")
    tu_genes = []
    for tu_component in tu_components:
        tu_component_parent_classes = pt_connection.get_frame_all_parents(tu_component)
        if "|All-Genes|" in tu_component_parent_classes:
            tu_genes.append(pt_connection.get_name_by_id(tu_component))
    tu_genes_by_function = pt_connection.transcription_unit_genes(tu_id)
    if not tu_genes_by_function:
        print(tu_id)
        print(f"\t{tu_genes}")
        print(f"\t{tu_genes_by_function}")