def get_regulondb_genes(gene_ids=None, only_properties_with_values=False):
    from ecocyc_extractor.ecocyc.collections.genes import Genes
    genes = Genes(gene_ids)

    for gene in genes.objects:
        gene_object = {
            "_id": gene.id,
            "bnumber": gene.bnumber,
            "centisomePosition": gene.centisome_position,
            "citations": gene.citations,
            "externalCrossReferences": gene.db_links,
            "fragments": gene.fragments,
            "gcContent": gene.gc_content,
            "internalComment": gene.internal_comment,
            "interrupted": gene.interrupted,
            "leftEndPosition": gene.left_end_position,
            "name": gene.name,
            "note": gene.comment,
            "organism_id": gene.organism,
            "rightEndPosition": gene.right_end_position,
            "sequence": gene.sequence,
            "strand": gene.strand,
            "synonyms": gene.synonyms,
            "terms": gene.terms,
            "type": gene.type
        }
        if only_properties_with_values is True:
            gene_object = gene.get_only_properties_with_values(gene_object)
        yield gene_object

