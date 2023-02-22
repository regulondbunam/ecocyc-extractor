import os

# ecocyc object properties

ORGANISM_ID = os.getenv("ORGANISM")

ABBREV_NAME = "abbrev_name"
ABSOLUTE_CENTER_POSITION = "abs_center_pos"
ABSOLUTE_PLUS_1_POS = "absolute_plus_1_pos"
ACCESSION_1 = "accession_1"
ALTERNATE_SEQUENCE = "alternate_sequence"
ANTICODON = "anticodon"
ASSOCIATED_BINDING_SITE = "associated_binding_site"
ATTACHED_GROUP = "attached_group"
AUTHORS = "authors"
BINDS_SIGMA_FACTOR = "binds_sigma_factor"
CATALYZES = "catalyzes"
CENTISOME_POSITION = "centisome_position"
CITATIONS = "citations"
CODING_SEGMENTS = "coding_segments"
CONSENSUS_SEQUENCE = "consensus_sequence"
COMMENT = "comment"
COMPONENT_OF = "component_of"
COMPONENTS = "components"
DATA_SOURCE = "data_source"
DBLINKS = "dblinks"
DEFINITION = "definition"
DESCRIPTION = "description"
DNA_FOOTPRINT_SIZE = "dna_footprint_size"
FEATURE_COLOR = "feature_color"
FEATURES = "features"
FEATURE_OF = "feature_of"
FRAGMENTS = "fragments"
GENE = "gene"
GO_TERMS = "go_terms"
HOMOLOGY_MOTIF = "homology_motif"
ID = "frameid"
INTERRUPTED = "interrupted_p"
INTERNAL_COMMENT = "internal_comment"
ISOELECTRIC_POINT = "pi"
INVOLVED_IN_REGULATION = "involved_in_regulation"
LEND = "left_end_position"
LOCATIONS = "locations"
MEDLINE_ID = "medline_uid"
MINUS_10_LEFT = "minus_10_left"
MINUS_10_RIGHT = "minus_10_right"
MINUS_35_LEFT = "minus_35_left"
MINUS_35_RIGHT = "minus_35_right"
MODE = "mode"
MODIFIED_FORM = "modified_form"
MOLECULAR_WEIGHT_SEQ = "molecular_weight_seq"
MOLECULAR_WEIGHT_KD = "molecular_weight_kd"
NAME = "common_name"
TERMS = "terms"

PERTAINS_TO = "pertains_to"
PROMOTER_BOXES = "promoter_boxes"
PUBMED_ID = "pubmed_id"
REGULATES = "regulates"
REGULATED_ENTITY = "regulated_entity"
REGULATOR = "regulator"
REND = "right_end_position"
RESIDUE_NUMBER = "residue_number"
SCORE = "score"
SITE_LENGTH = "site_length"
SOURCE = "source"
SPLICE_FORM_INTRONS = "splice_form_introns"
STATIC_SEARCH_URL = "static_search_url"
SYMMETRY = "symmetry"
SYNONYMS = "synonyms"
TERM_MEMBERS = "term_members"
TITLE = "title"
TRANSCRIPTION_DIRECTION = "transcription_direction"
UNMODIFIED_FORM = "unmodified_form"
URL = "url"
YEAR = "year"
TYPE = "type"
CROSS_EVIDENCE_CODE_RULE = "cross_evidence_eode_rule"
EVIDENCE_CLASS_PROPERTY = "evidence_class"
EVIDENCE_CATEGORY = "evidence_category"
EVIDENCE_APPROACH = "evidence_approach"
NOTE_WEB = "note_web"
CONFIDENCE_LEVEL = "confidence_level"

# ecocyc classes' names
ALLOSTERIC_REGULATION_OF_RNAP = "|Allosteric-Regulation-of-RNAP|"
COMPOUNDS_CLASS = "|Compounds|"
CRYPTIC_PROPHAGES = "|Cryptic-Prophages|"
EVIDENCE_CLASS = "|Evidence|"
EXTERNAL_DB_CLASS = "|Databases|"
GENE_CLASS = "|All-Genes|"
GO_TERMS_CLASS = "|Gene-Ontology-Terms|"
MACROMOLECULES_CLASS = "|Macromolecules|"
MULTIFUN_CLASS = "|MultiFun|"
POLYPEPTIDE_CLASS = "|Polypeptides|"
PROTEIN_COMPLEXES_CLASS = "|Protein-Complexes|"
PROTEIN_SMC_CLASS = "|Protein-Small-Molecule-Complexes|"
PSEUDO_PRODUCT_CLASS = "|Pseudo-Products|"
PUBLICATIONS_CLASS = "|Publications|"
PROTEIN_CLASSES = [
    POLYPEPTIDE_CLASS,
    PROTEIN_COMPLEXES_CLASS,
    PROTEIN_SMC_CLASS,
    PSEUDO_PRODUCT_CLASS,
]
TERMINATOR_CLASS = "|Terminators|"
TRANSCRIPTION_UNIT_CLASS = "|Transcription-Units|"
PROMOTER_CLASS = "|Promoters|"
TRANSCRIPTION_FACTOR_BINDING_CLASS = "|Transcription-Factor-Binding|"
RHO_INDEPENDENT = "|Rho-Independent-Terminators|"
RHO_DEPENDENT = "|Rho-Dependent-Terminators|"
RNAS = "|RNAs|"
DNA_SEGMENTS = "|DNA-Segments|"
MRNA_SEGMENTS = "|mRNA-Segments|"
# SLOTS through slot value

ABSOLUTE_PLUS_1_POS_SLOT = "|ABSOLUTE-PLUS-1-POS|"
ABSOLUTE_CENTER_POSITION_SLOT = "|ABS-CENTER-POS|"
ASSOCIATED_BINDING_SITE_SLOT = "|ASSOCIATED-BINDING-SITE|"
BINDS_SIGMA_FACTOR_SLOT = "|BINDS-SIGMA-FACTOR|"
CITATIONS_SLOT = "|CITATIONS|"
COMMON_NAME_SLOT = "|COMMON-NAME|"
DBLINKS_SLOT = "|DBLINKS|"
FRAGMENTS_SLOT = "|FRAGMENTS|"
FRAGMENT_OF_SLOT = "|FRAGMENT-OF|"
GO_TERMS_SLOT = "|GO-TERMS|"
LEND_SLOT = "|LEFT-END-POSITION|"
MODE_SLOT = "|MODE|"
PM_PROMOTER_FEATURE_ID_SLOT = "|PROMOTER-BOXES|"
PRODUCT_MOTIF_ID_SLOT = "|FEATURES|"
REGULATES_SLOT = "|REGULATES|"
REGULATOR_SLOT = "|REGULATOR|"
RI_SITE_ID_SLOT = "|ASSOCIATED-BINDING-SITE|"
REND_SLOT = "|RIGHT-END-POSITION|"
TRANSCRIPTION_DIRECTION_SLOT = "|TRANSCRIPTION-DIRECTION|"
COMPONENT_OF_SLOT = "|COMPONENT-OF|"
REGULATED_ENTITY_SLOT = "|REGULATED-ENTITY|"

# SLOT "CLASSES"
SLOT_COMPONENTS_CLASS = "|COMPONENTS|"
SLOT_COEFFICIENT_CLASS = "|COEFFICIENT|"
SLOT_GENE_CLASS = "|GENE|"
SLOT_PRODUCT_CLASS = "|PRODUCT|"
SLOT_UNMODIFIED_FORM_CLASS = "|UNMODIFIED-FORM|"
SLOT_FEATURE_CLASS = "|FEATURES|"


GENES = "|Genes|"
PHANTOM_GENES = "|Phantom-Genes|"
PSEUDO_GENES = "|Pseudo-Genes|"
TRUNCATED_GENES = "|Truncated-Genes|"
DNA_BINDING_SITES = "|DNA-Binding-Sites|"
EXTRAGENIC_SITES = "|Extragenic-Sites|"
GENE_FRAGMENTS = "|Gene-Fragments|"
GENOMIC_ISLANDS = "|Genomic-Islands|"
MISC_FEATURES = "|Misc-Features|"
PROPHAGES = "|Prophages|"
REPLICON_BUCKETS = "|Replicon-Buckets|"
RECOMBINATION_SITES = "|Recombination-Sites|"
SPNS = "|SPNs|"
MRNA_BINDING_SITES = "|mRNA-Binding-Sites|"
TRANSPOSONS = "|Transposons|"

RNA_MEDIATED_TRANSLATION_REGULATION = "|RNA-Mediated-Translation-Regulation|"
PROTEIN_MEDIATED_TRANSLATION_REGULATION = "|Protein-Mediated-Translation-Regulation|"
REGULATION_OF_TRANSLATION = "|Regulation-of-Translation|"
REGULATION_OF_TRANSCRIPTION = "|Regulation-of-Transcription|"
MECHANISM = "mechanism"
INVOLVED_IN_REGULATION = "Involved-In-Regulation"
POLYMER_SEGMENTS = "|Polymer-Segments|"

ACCESSORY_PROTEINS = "|Accessory-Proteins|"
REGULATION_TYPE = "|Regulation-Type|"
DISTANCE_TO_GENE = "|Distance-To-Gene|"

# MG Collections
# COLLECTIONS NAMES
EV_COLLECTION = "evidences"
EXREF_COLLECTION = "externalCrossReferences"
GENE_COLLECTION = "genes"
MOTIF_COLLECTION = "motif"
ONTOLOGIES_COLLECTION = "ontologies"
OPERONS_COLLECTION = "operons"
ORGANISMS_COLLECTION = "organisms"
PRODUCTS_COLLECTION = "products"
PROMOTERS_COLLECTION = "promoters"
PUB_COLLECTION = "publications"
RCPLX_COLLECTION = "regulatoryComplexes"
RCONT_COLLECTION = "regulatoryContinuants"
RI_COLLECTION = "regulatoryInteractions"
RST_COLLECTION = "regulatorySites"
SEGMENTS_COLLECTION = "segments"
SIGMA_FACTORS_COLLECTION = "sigmaFactors"
TERMONATORS_COLLECTION = "terminators"
TERMS_COLLECTION = "terms"
TF_COLLECTION = "transcriptionFactors"
TU_COLLECTION = "transcriptionUnits"
# SUB_COLLECTIONS
PROTEIN_COMPLEXES_COLLECTION = "proteinComplexes"
MOD_PROTEIN_COLLECTION = "modifiedProteins"
SMALL_MOLECULE_COMPLEX_COLLECTION = "smallMoleculeComplex"
