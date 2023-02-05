# Ecocyc Extractor Changelog

This version is in testing process with new Ecocyc release 26.5 for the RegulonDB 11.2 release.

## [1.0.1](https://github.com/regulondbunam/ecocyc-extractor/releases/tag/1.0.1) - 2023-02-04

### Added

- Testing modules
  - Module checks functions works for debogging porposes.
  - Module can test if there where minor changes in the extracted collections related to the collections in our database based on the IDs registered.
  - The module was tested with Python [**unittest**](https://docs.python.org/3/library/unittest.html) and [**PyTest**](https://docs.pytest.org/en/7.2.x/) frameworks

### Changed

- Some files has modifications in the import statements for testing porposes, it does not affect the code execution and will be implemented eventually in the rest of the files.
  - ecocyc_extractor/ecocyc/collections/evidences.py
  - ecocyc_extractor/ecocyc/collections/external_databases.py
  - ecocyc_extractor/ecocyc/collections/genes.py
  - ecocyc_extractor/ecocyc/domain/base.py
  - ecocyc_extractor/ecocyc/utils/constants.py
  - ecocyc_extractor/ecocyc/utils/pathway_tools/connection.py

### Deprecated

- Without changes.

### Fixed

- Readme badges versions and links update and orthographics corrections.
- Snakefile has a block of code commented.
