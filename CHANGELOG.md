# Ecocyc Extractor Changelog

This version is in testing process with new Ecocyc release 26.5 for the RegulonDB 11.2 release.

## [1.0.2](https://github.com/regulondbunam/ecocyc-extractor/releases/tag/1.0.2) - 2023-02-13

### Added

- Without changes.

### Changed

- Files modified in this patch.
  - [`CHANGELOG.md`](CHANGELOG.md)
  - [`README.md`](README.md)
  - [`ecocyc_extractor/__main__.py`](ecocyc_extractor/__main__.py)
  - [`ecocyc_extractor/ecocyc/collections/evidences.py`](ecocyc_extractor/ecocyc/collections/evidences.py)
  - [`ecocyc_extractor/ecocyc/domain/evidence.py`](ecocyc_extractor/ecocyc/domain/evidence.py)
  - [`ecocyc_extractor/ecocyc/domain/product.py`](ecocyc_extractor/ecocyc/domain/product.py)
- New Evidence Code generation, now is generated using the Evidence ID.

### Deprecated

- Old Evidence Code generation, Code was generated using the Evidence name.

### Fixed

- Readme badges CHANGELOG link update.
- Products Crash.
- There was a problem with the product extraction:
  - This error occurred when trying to get the term_genbank_feature of a Product term when calling the map_go_term_genbank_feature() function of the pathwaytools pythoncyc API. This function seems to return the term feature mapped to genbank. The possible results are:
    go_process
    go_component
    go_function
    This indicates that possibly the terms that cause the error are not mapped with genebank or something similar, it should be noted that in version 26.0 of Ecocyc these GOTerms already existed, for now the IDs of the Products were captured with the terms that caused the failure to Determine what to do with them.
- There was an unnecessary print in the evidence extraction.
