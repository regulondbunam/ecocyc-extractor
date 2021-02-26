import pythoncyc
import json

pt_conn = pythoncyc.select_organism("ecoli")

dna_segments_ids = pt_conn.get_class_all_instances("|DNA-Segments|")
mrna_segments_ids = pt_conn.get_class_all_instances("|mRNA-Segments|")

# print(dna_segments_ids)
# print(mrna_segments_ids)

for segment_id in mrna_segments_ids:
    parent_id = pt_conn.get_frame_all_parents(segment_id)
    if '|mRNA-Segments|' in parent_id:
        print(segment_id, ' my parent: ', parent_id)

print("--------------------------------\n")
with open("dna_segments.json", "w") as outfile:
    json.dump(dna_segments_ids, outfile, indent=4)

print("--------------------------------\n")
with open("mrna_segments.json", "w") as outfile:
    json.dump(mrna_segments_ids, outfile, indent=4)

segments_ids = dna_segments_ids + mrna_segments_ids

print("--------------------------------\n")
with open("segments.json", "w") as outfile:
    json.dump(segments_ids, outfile, indent=4)
