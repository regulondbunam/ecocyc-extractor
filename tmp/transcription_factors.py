import pythoncyc

pt_conn = pythoncyc.select_organism("ecoli")


def get_regulators_by(regulatory_interaction_ids: list) -> list:
    regulator_ids = []
    for ri_id in regulatory_interaction_ids:
        regulator_id = pt_conn.get_slot_value(ri_id, "|REGULATOR|")
        if regulator_id:
            regulator_ids.append(regulator_id)
    regulator_ids = list(set(regulator_ids))
    return regulator_ids


def get_regulator_transcription_factors_mapping_by(regulator_ids: list) -> dict:
    regulators_tfs = {}
    for regulator_id in regulator_ids:
        monomer_ids = pt_conn.monomers_of_protein(regulator_id, unmodify=True)
        if not monomer_ids:
            regulators_tfs[regulator_id] = regulator_id
        if len(monomer_ids) == 1:
            # CPLX0-#### -> [PD00242]
            regulators_tfs[regulator_id] = monomer_ids[0]
        elif len(monomer_ids) > 1:
            # CPLX0-1234(GadE-RcsB) -> [PD00123, PD0231]
            regulators_tfs[regulator_id] = regulator_id
    return regulators_tfs


def get_transcription_factors_regulator_mapping_by(regulator_ids: list) -> dict:
    tfs_regulators = {}
    # {"AraC": ["AraC"]}
    for regulator_id in regulator_ids:
        monomer_ids = pt_conn.monomers_of_protein(regulator_id, unmodify=True)
        if not monomer_ids:
            tfs_regulators.setdefault(regulator_id, []).append(regulator_id)
            #if regulator_id in regulators_tfs:
            #    regulators_tfs[regulator_id].append(regulator_id)
            #else:
            #    regulators_tfs[regulator_id] = [regulator_id]
        if len(monomer_ids) == 1:
            # CPLX0-#### -> [PD00242]
            tfs_regulators.setdefault(monomer_ids[0], []).append(regulator_id)
        elif len(monomer_ids) > 1:
            # CPLX0-1234(GadE-RcsB) -> [PD00123, PD0231]
            tfs_regulators.setdefault(regulator_id, []).append(regulator_id)
    return tfs_regulators


def get_regulated_genes_by_promoter(_id: str) -> list:
    tu_ids = pt_conn.transcription_units_of_promoter(_id)
    promoter_genes = []
    for tu_id in tu_ids:
        tu_genes = get_regulated_genes_by_transcription_unit(tu_id)
        if tu_genes:
            promoter_genes.extend(tu_genes)
    promoter_genes = list(set(promoter_genes))
    return promoter_genes


def get_regulated_genes_by_transcription_unit(_id: str) -> list:
    return pt_conn.transcription_unit_genes(_id)


def get_regulated_genes_by_regulated_entity(_id: str) -> list:
    if _id:
        re_parents = pt_conn.get_frame_all_parents(_id)
        if "|Promoters|" in re_parents:
            return get_regulated_genes_by_promoter(_id)
        elif "|Transcription-Units|" in re_parents:
            return get_regulated_genes_by_transcription_unit(_id)
        else:
            raise NotImplementedError("No se ha implementado logica para este tipo de regulated entity")
    return []


def get_tfs_genes_mapping_by(ri_ids: list, regulator_tfs: dict) -> dict:
    tfs_genes = {}
    for ri_id in ri_ids:
        regulated_entity_id = pt_conn.get_slot_value(ri_id, "|REGULATED-ENTITY|")
        regulator_id = pt_conn.get_slot_value(ri_id, "|REGULATOR|")
        genes = get_regulated_genes_by_regulated_entity(regulated_entity_id)
        if regulator_id:
            tf = regulator_tfs[regulator_id]
            tfs_genes.setdefault(tf, []).extend(genes)
            tfs_genes[tf] = list(set(tfs_genes[tf]))
    return tfs_genes


def get_tf_name_by_transcription_factor(_id: str) -> str:
    abbreviated_name = pt_conn.get_slot_value(_id, "|ABBREV-NAME|")
    if abbreviated_name:
        return abbreviated_name
    return pt_conn.get_slot_value(_id, "|COMMON-NAME|")


def get_unique_gene_names_by(gene_ids: list) -> list:
    return list(set([pt_conn.get_name_by_id(gene_id) for gene_id in gene_ids]))


if __name__ == '__main__':

    regulatory_interaction_ids = pt_conn.get_class_all_instances("|Transcription-Factor-Binding|")

    regulator_ids = get_regulators_by(regulatory_interaction_ids)

    regulators_tfs = get_regulator_transcription_factors_mapping_by(regulator_ids)

    tfs_genes = get_tfs_genes_mapping_by(regulatory_interaction_ids, regulators_tfs)

    for tf_id, gene_ids in tfs_genes.items():
        tf_name = get_tf_name_by_transcription_factor(tf_id)
        gene_names = get_unique_gene_names_by(gene_ids)
        print(tf_name, tf_id)
        print(f"\t{len(gene_names)}")