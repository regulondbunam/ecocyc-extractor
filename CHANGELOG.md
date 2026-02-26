# Ecocyc Extractor Changelog

This version updates the extraction process for the new EcoCyc release **29.5**, aligned with the **RegulonDB 14.5** release.

---

## [2.1.2](https://github.com/regulondbunam/ecocyc-extractor/releases/tag/2.1.2) - 2026-02-25

### Added
- Without changes.

### Changed
- Improved gene filtering logic in Transcription Unit (TU) computation to exclude genes associated with pseudo-gene categories such as `|Gene-Fragments|`.
  - Genes are now excluded if **any parent** in their parent list belongs to a pseudo-gene category.
  - Prevents pseudo-genes from being treated as canonical genes in `tu.gene_ids`.
- Products `Type` property now correctly maps `|Small-RNAs|` to `small RNA`.
  - Ensures proper classification of sRNA products during extraction.

### Fixed
- Propagated and mapped organism identifiers into the final organism domain object.
  - Fixes incomplete organism metadata emission in the extraction pipeline.
- Removed unused fields (`citations`, `db_links`) from the collection payload.
  - These properties were not referenced in the JSON Schema and were unnecessary in the domain model.

### Deprecated
- Without changes.

### To Fix
- Without changes.