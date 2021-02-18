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

# SLOTS through slot value

ABSOLUTE_PLUS_1_POS_SLOT = "|ABSOLUTE-PLUS-1-POS|"
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

# SLOT "CLASSES"
SLOT_COMPONENTS_CLASS = "|COMPONENTS|"
SLOT_COEFFICIENT_CLASS = "|COEFFICIENT|"
SLOT_GENE_CLASS = "|GENE|"
SLOT_PRODUCT_CLASS = "|PRODUCT|"
SLOT_UNMODIFIED_FORM_CLASS = "|UNMODIFIED-FORM|"
SLOT_FEATURE_CLASS = "|FEATURES|"
