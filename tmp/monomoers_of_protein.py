import pythoncyc

pt_conn = pythoncyc.select_organism("ecoli")

print(pt_conn.monomers_of_protein("|PHOSPHO-CPXR|", unmodify=True))