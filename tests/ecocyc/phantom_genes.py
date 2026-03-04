import pymongo


phantom_genes = ["RDBECOLIGNC01145", "RDBECOLIGNC01192", "RDBECOLIGNC01246", "RDBECOLIGNC02567", "RDBECOLIGNC02647", "RDBECOLIGNC02648", "RDBECOLIGNC02658", "RDBECOLIGNC02707", "RDBECOLIGNC02709", "RDBECOLIGNC02711", "RDBECOLIGNC02712", "RDBECOLIGNC02713", "RDBECOLIGNC02714", "RDBECOLIGNC02756", "RDBECOLIGNC02872", "RDBECOLIGNC02893", "RDBECOLIGNC02894", "RDBECOLIGNC02896", "RDBECOLIGNC02898", "RDBECOLIGNC02902"
                 ]


pseudo_genes = ["RDBECOLIGNC00008", "RDBECOLIGNC00393", "RDBECOLIGNC00651", "RDBECOLIGNC01079", "RDBECOLIGNC01255", "RDBECOLIGNC01276", "RDBECOLIGNC01352", "RDBECOLIGNC01451", "RDBECOLIGNC01649", "RDBECOLIGNC01700", "RDBECOLIGNC01704", "RDBECOLIGNC01709", "RDBECOLIGNC01711", "RDBECOLIGNC01852", "RDBECOLIGNC01908", "RDBECOLIGNC01934", "RDBECOLIGNC01960", "RDBECOLIGNC02052", "RDBECOLIGNC02053", "RDBECOLIGNC02090"
                ]

genes_ids = pseudo_genes
gene_type = 'pseudo_genes'
genes_ids = phantom_genes
gene_type = 'phantom_genes'

database = "regulondbmultigenomic"
url = "mongodb://localhost:27017/"

mongo_client = pymongo.MongoClient(url)
db = mongo_client['regulondbidentifiers']
collection = db["identifiers"]
query = {
    "objectOriginalSourceId": 'AE_ID(EXP-IDA-HPT-TRANSCR-INIT-M-RACE-MAP/COMP-AINF)'}
id_objs = collection.find_one(query)
print(id_objs)
exit()

gene_names = [
    "tmk",
    "garD",
    "rffC",
    "ykfL",
    "ybhU",
    "G6084",
    "isrB",
    "insB7",
    "ycdF",
    "sroG",
    "G6294",
    "IS128",
    "G0-10700",
    "G7121",
    "b0105",
    "G7034",
    "b4700",
    "yeeH",
    "yibU",
    "yzfA",
    "b1052",
    "G6690",
    "sroD",
    "yjhY",
    "ybfK",
    "yehH",
    "psaA",
    "insM",
    "yjgW",
    "C0362",
    "sraF",
    "istR-1",
    "glvG",
    "ygiA",
    "G8203",
    "yicT",
    "C0719",
    "G6678",
    "G0-10702",
    "C0465",
    "mokA",
    "yrhC",
    "b3254",
    "b0309",
    "ysaD",
    "G6336",
    "ryfB",
    "b2191",
    "yrdF",
    "ykgQ",
    "insX",
    "yoeH",
    "ykfK",
    "peaD",
    "yjdQ",
    "G7353",
    "b0165",
    "yoeD",
    "b1364",
    "G7881",
    "G0-10698",
    "G6748",
    "G0-10705",
    "yrdE",
    "b0725",
    "C0664",
    "tpke70",
    "G6740",
    "yoeG",
    "fruL",
    "b2651",
    "ysaC",
    "yliL",
    "C0614",
    "G0-10703",
    "G0-10704",
    "b0100",
    "ackB",
    "G7562",
    "insI2",
    "yncK",
    "G0-10697",
    "pawZ",
    "tisA",
    "ykiB",
    "G7388",
    "yibW",
    "G7818",
    "tpke11",
    "C0067",
    "sokA",
    "G7878",
    "G7561",
    "C0299",
    "cybC",
    "ybfI",
    "tfaS",
    "tp2"
]

collection = db["genes"]
genes_ids = []
gene_type = "Asna"
for gene_name in gene_names:
    query = {"name": gene_name}
    gene_obj = collection.find(query)
    for gene in gene_obj:
        genes_ids.append({'name': gene_name, '_id': gene.get('_id')})

collection = db["products"]


print(f'Genes Type {gene_type}')
for gene_id in genes_ids:
    query = {"genes_id": gene_id.get("_id"), }
    products = collection.find(query)
    products_of_gene = []
    for product in products:
        if product is not None:
            products_of_gene.append(product.get('_id'))
    print(f'GeneID: {gene_id} products:{products_of_gene}')
