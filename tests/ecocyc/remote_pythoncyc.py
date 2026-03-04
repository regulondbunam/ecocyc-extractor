import pythoncyc
from pythoncyc import config as pconfig


pconfig.set_host_name("127.0.0.1")
pconfig.set_host_port(5008)

orgs = pythoncyc.all_orgids()
print(orgs)

GENE_CLASS = "|All-Genes|"

for org in orgs:
    ecoli = pythoncyc.select_organism('|ECOLI|')
    print(ecoli.all_operons())
    print(ecoli.get_class_all_instances(GENE_CLASS[:10]))
