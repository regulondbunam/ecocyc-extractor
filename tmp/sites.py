import pythoncyc

pt_connection = pythoncyc.select_organism("ecoli")

ri_ids = pt_connection.get_class_all_instances("|Transcription-Factor-Binding|")

site_ids = []
for ri_id in ri_ids:
    site_id = pt_connection.get_slot_value(ri_id, "|ASSOCIATED-BINDING-SITE|")

    if site_id not in site_ids:
        site_ids.append(site_id)
    else:
        print("ya estoy: ", site_id)
