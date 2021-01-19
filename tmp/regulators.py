import pythoncyc

pt_connection = pythoncyc.select_organism('ecoli')

ri_ids = pt_connection.get_class_all_instances('|Transcription-Factor-Binding|')

regulator_classes = []
for ri_id in ri_ids:
    regulator = pt_connection.get_slot_value(ri_id, '|REGULATOR|')
    if regulator:
        regulator_class = pt_connection.get_frame_all_parents(regulator)
        regulator_classes.append(regulator_class[-1])

regulator_classes = set(regulator_classes)
print(len(pt_connection.all_transcription_factors(allow_modified_forms=False)))
