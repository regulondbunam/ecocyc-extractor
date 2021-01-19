import identifiers_api

identifiers_api.connect("mongodb://127.0.0.1:27017/")

source_id = "TEMP5ccca9366e06251414ea6a2c"
source_id = "|REG0-11519|"

regulondb_id = identifiers_api.get_identifier_by(source_id, "ECOLI", "regulatoryInteractions")
print("valor de regulondb_id", regulondb_id)
if regulondb_id:
    print("entro a procesar")
else:
    print("envio a json de archivos no registrados")
