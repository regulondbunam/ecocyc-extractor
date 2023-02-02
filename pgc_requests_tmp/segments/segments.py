import pythoncyc
import json

pt_conn = pythoncyc.select_organism("ecoli")

genes_ids = pt_conn.get_class_all_instances("|Genes|")
#print(genes_ids)

gene_by_pos = pt_conn.find_prev_gene(4266861, '|ECOLI|')
print(gene_by_pos)

gene_by_pos = pt_conn.find_next_gene(4266861, '|ECOLI|')
print(gene_by_pos)

gene_by_pos = pt_conn.find_neighbor_gene(70387, 71265, '|ECOLI|')
print(gene_by_pos)







'''mrna_segments_ids = pt_conn.get_class_all_instances("|mRNA-Segments|")

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

'''