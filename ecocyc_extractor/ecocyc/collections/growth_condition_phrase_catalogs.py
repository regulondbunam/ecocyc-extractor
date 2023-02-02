import logging

from ecocyc.utils.pathway_tools.connection import Connection
from ecocyc.utils import constants as EC, utils
from ecocyc.utils.growth_conditions_extractor import McoTmp
from ecocyc.domain.growth_condition_phrase_catalog import GrowthConditionPhraseCatalog


class GrowthConditionPhraseCatalogs(object):
    # TODO: Create an algorithm that extract GrowthConditionPhrases
    pt_connection = Connection()

    def get_object_type(parent_classes):
        if "|Promoters|" in parent_classes:
            return "Promoter"
        if "|Transcription-Units|" in parent_classes:
            return "Transcription-Unit"
        if "|All-Genes|" in parent_classes:
            return "Gene"

    def __init__(self, ids=None):
        self.ids = GrowthConditionPhraseCatalogs.get_ids(ids)

    @staticmethod
    def get_ids(gcpc_ids=None):
        if gcpc_ids is None:
            gcpc_ids = []
            # GETTTING FROM TRANSCRIPTION_FACTOR_BINDING IDs
            ri_tfb_ids = GrowthConditionPhraseCatalogs.pt_connection.get_class_all_instances(
                EC.TRANSCRIPTION_FACTOR_BINDING_CLASS)
            ri_tfb_objects = GrowthConditionPhraseCatalogs.pt_connection.get_frame_objects(
                ri_tfb_ids)
            for ri_tfb_object in ri_tfb_objects:
                ri_regulated_entity = ri_tfb_object["regulated_entity"]
                if ri_regulated_entity is None:
                    continue
                ri_regulated_entity_parent_classes = GrowthConditionPhraseCatalogs.pt_connection.get_frame_all_parents(
                    ri_regulated_entity)
                object_type = GrowthConditionPhraseCatalogs.get_object_type(
                    ri_regulated_entity_parent_classes)
                regulondb_id = ri_tfb_object["frameid"]
                comments = ri_tfb_object["comment"]
                gc_slot = ri_tfb_object["growth_conditions"]
                #print('GC Slot >> ', gc_slot, regulondb_id)

                if comments:
                    for comment in comments:
                        growth_condition = utils.get_growth_condition_from_comment(
                            comment, regulondb_id)
                        if growth_condition:
                            gcpc_ids.extend(growth_condition)
                if gc_slot:
                    gcpc_ids.extend(utils.transform_growth_conditions(gc_slot))

            growth_conditions = McoTmp(
                regulondb_id, ri_tfb_object, object_type, GrowthConditionPhraseCatalogs.pt_connection)
            if growth_conditions():
                pass
                #print(f'-GC_OBJ-{growth_conditions()} \n -COMMENT-{comment} \n -GC_RAW-{gc_slot}')

            # GETTTING FROM ALLOSTERIC_REGULATION_OF_RNAP IDs
            ri_arr_ids = GrowthConditionPhraseCatalogs.pt_connection.get_class_all_instances(
                EC.ALLOSTERIC_REGULATION_OF_RNAP)
            ri_arr_objects = GrowthConditionPhraseCatalogs.pt_connection.get_frame_objects(
                ri_arr_ids)
            for ri_arr_object in ri_arr_objects:
                object_type = GrowthConditionPhraseCatalogs.get_object_type(
                    ri_regulated_entity_parent_classes)
                regulondb_id = ri_arr_object["frameid"]
                object_type = "ppGpp"
                comment = ri_arr_object["comment"]
                gc_slot = ri_arr_object["growth_conditions"]
                #print('GC Slot >> ', gc_slot, regulondb_id)
                if comments:
                    for comment in comments:
                        growth_condition = utils.get_growth_condition_from_comment(
                            comment, regulondb_id)
                        if growth_condition:
                            gcpc_ids.extend(growth_condition)
                if gc_slot:
                    gcpc_ids.extend(utils.transform_growth_conditions(gc_slot))

            gcpc_ids = list(dict.fromkeys(gcpc_ids))

            '''for gcpc_id in gcpc_ids:
                print(gcpc_id)'''
            # exit(0)
            # GETTTING FROM RNA_MEDIATED_TRANSLATION_REGULATION IDs
            # ri_rna_ids = GrowthConditionPhraseCatalogs.pt_connection.get_class_all_instances(EC.RNA_MEDIATED_TRANSLATION_REGULATION)
            # GETTTING FROM PROTEIN_MEDIATED_TRANSLATION_REGULATION IDs
            # ri_prot_ids = GrowthConditionPhraseCatalogs.pt_connection.get_class_all_instances(EC.PROTEIN_MEDIATED_TRANSLATION_REGULATION)

        else:
            gcpc_ids = None
        gcpc_ids = utils.get_unique_elements(gcpc_ids)
        return gcpc_ids

    @property
    def objects(self):
        for gc_phrase in self.ids:
            gc_terms = gc_phrase.split('|')
            print(gc_terms)
        gene_objects = GrowthConditionPhraseCatalogs.pt_connection.get_frame_objects(
            self.ids)
        for growth_condition_phrase_catalog in gene_objects:
            growth_condition_phrase_catalog = GrowthConditionPhraseCatalogs.set_gcpc(
                growth_condition_phrase_catalog)
            logging.info(
                f'Working on Growth Condition Phrase Catalog: {growth_condition_phrase_catalog["id"]}')
            ecocyc_gcpc = GrowthConditionPhraseCatalog(
                **growth_condition_phrase_catalog)
            yield ecocyc_gcpc

    @staticmethod
    def set_gcpc(growth_condition_phrase_catalog):
        new_gcpc = dict(
            id=growth_condition_phrase_catalog[EC.ID],
            description=growth_condition_phrase_catalog[EC.DESCRIPTION],
            name=growth_condition_phrase_catalog[EC.NAME],
            terms=growth_condition_phrase_catalog[EC.TERMS]
        )
        return new_gcpc
