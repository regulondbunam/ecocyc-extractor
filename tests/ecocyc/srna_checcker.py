import pythoncyc
from pythoncyc import config as pconfig
import pandas as pd


pconfig.set_host_name("127.0.0.1")
pconfig.set_host_port(5008)

RNA_CLASSES = [
    "|All-tRNAs|",
    "|rRNAs|",
    "|snRNAs|",
    "|tmRNAs|",
    "|Regulatory-RNAs|",
    "|Misc-RNAs|",
    "|Small-RNAs|"

]
ORGANISM_ID = '|ECOLI|'
connection = pythoncyc.select_organism(ORGANISM_ID)

rows = []
for RNA_CLASS in RNA_CLASSES:
    class_content = connection.get_class_all_instances(RNA_CLASS)
    rows.append({
        "RNA_CLASS_ID" : RNA_CLASS,
        "CONTENT" : list(class_content)
    })
    
data_f = pd.DataFrame(rows)

data_f.to_csv('tests/ecocyc/rnas_content.csv', index=False)
