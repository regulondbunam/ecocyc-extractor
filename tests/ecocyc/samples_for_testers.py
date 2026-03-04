#!/usr/bin/env python3
"""
Extract random samples per type from regulondbidentifiers.identifiers
and export them as Python global variables.
"""

from pymongo import MongoClient
from collections import defaultdict
import re

# --------------------------------------------------
# Config
# --------------------------------------------------

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "regulondbidentifiers"
COLLECTION_NAME = "identifiers"

OUTPUT_FILE = "identifier_samples.py"
SAMPLE_SIZE = 25

PROJECTING = "objectOriginalSourceId"


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def to_python_var(name: str) -> str:
    """
    Convert Mongo type names into safe Python variable names.
    """
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return f"{name}_ids".upper()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    print("Getting distinct types...")
    types = collection.distinct("type")

    results = defaultdict(list)

    for i, t in enumerate(types, start=1):
        print(f"[{i}/{len(types)}] Sampling type: {t}")

        pipeline = [
            {"$match": {"type": t}},
            {"$sample": {"size": SAMPLE_SIZE}},
            {"$project": {PROJECTING: 1, "_id": 0}},
        ]

        docs = list(collection.aggregate(pipeline))
        results[t] = [str(doc[PROJECTING]) for doc in docs if PROJECTING in doc]

    print(f"Writing output -> {OUTPUT_FILE}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Auto-generated file\n")
        f.write("# Random samples per type\n\n")

        # Variables globales
        for t, ids in results.items():
            var_name = to_python_var(t)
            f.write(f"{var_name} = {ids}\n\n")

        # Diccionario global útil para tests
        f.write("SAMPLE_IDS_BY_TYPE = {\n")
        for t in results:
            var_name = to_python_var(t)
            f.write(f"    '{t}': {var_name},\n")
        f.write("}\n")

    print("Done ✅")


if __name__ == "__main__":
    main()
