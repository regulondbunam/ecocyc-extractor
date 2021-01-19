import pythoncyc

pt_connection = pythoncyc.select_organism('ecoli')

ri_ids = pt_connection.get_class_all_instances("|Transcription-Factor-Binding|")
protein_genes = {}

for ri_id in ri_ids[0:10]+["|REG0-10592|", "|REG0-4764|"]:
    genes = []
    regulator = pt_connection.get_slot_value(ri_id, "|REGULATOR|")
    regulated_entity = pt_connection.get_slot_value(ri_id, "|REGULATED-ENTITY|")

    if regulator and regulated_entity:

        regulator_name = pt_connection.get_slot_value(regulator, "|COMMON-NAME|")

        re_parent_classes = pt_connection.get_frame_all_parents(regulated_entity)
        if "|Promoters|" in re_parent_classes:
            # Obteniendo los componentes del promotor
            re_component_of = pt_connection.get_slot_values(regulated_entity, "|COMPONENT-OF|")
            # Iterando los componentes del promotor
            for pm_re_component_of_id in re_component_of: #[ECOLI-123, |TU-12314|]
                # Obteniendo las clases papa del componente iterado
                pm_component_parent_classes = pt_connection.get_frame_all_parents(pm_re_component_of_id)
                # Filtrando solo los componentes del promotor que son de tipo TU
                if "|Transcription-Units|" in pm_component_parent_classes:

                    tu_components = pt_connection.get_slot_values(pm_re_component_of_id, "|COMPONENTS|")
                    for tu_component_id in tu_components:
                        tu_component_parent_classes = pt_connection.get_frame_all_parents(tu_component_id)
                        if "|All-Genes|" in tu_component_parent_classes:
                            gene_name = pt_connection.get_name_by_id(tu_component_id)
                            genes.append(gene_name)
        elif "|Transcription-Units|" in re_parent_classes:
            tu_components = pt_connection.get_slot_values(regulated_entity, "|COMPONENTS|")
            for tu_component_id in tu_components:
                tu_component_parent_classes = pt_connection.get_frame_all_parents(
                    tu_component_id)
                if "|All-Genes|" in tu_component_parent_classes:
                    gene_name = pt_connection.get_name_by_id(tu_component_id)
                    genes.append(gene_name)

        else:
            raise NotImplementedError("No se ha implementado logica para este tipo de Regulated Entity")
        # implementar logica para obtener TF y a eso mapear los genes
        protein_genes.setdefault(regulator_name, []).extend(genes)
    #print(regulator, genes)

for protein_name, genes_regulated in protein_genes.items():
    print(protein_name)
    print(f"\t {set(genes_regulated)}")

# Functional
# OOP
