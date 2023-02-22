# Ecocyc Extractor Changelog

This version is in testing process with new Ecocyc release 26.5 for the RegulonDB 11.2 release.

## [1.0.3](https://github.com/regulondbunam/ecocyc-extractor/releases/tag/1.0.3) - 2023-02-22

### Added

- New Evidence properties added.
  - type
  - crossEvidenceCodeRule
  - evidenceClass
  - evidenceCategory
  - evidenceApproach
  - noteWeb
  
### Changed

- Files modified in this patch.
  - [`ecocyc_extractor/ecocyc/collections/evidences.py`](ecocyc_extractor/ecocyc/collections/evidences.py)
  - [`ecocyc_extractor/ecocyc/domain/evidence.py`](ecocyc_extractor/ecocyc/domain/evidence.py)
  - [`ecocyc_extractor/ecocyc/utils/constants.py`](ecocyc_extractor/ecocyc/utils/constants.py)
  - [`ecocyc_extractor/regulondb/evidences.py`](ecocyc_extractor/regulondb/evidences.py)
- The Evidence properties where added for future Ecocyc releases, these changes is to maintain parity with the MultigenomicModel

### Deprecated

- Without changes.

### Fixed

- Without changes.
