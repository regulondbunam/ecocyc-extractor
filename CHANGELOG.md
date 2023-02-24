# Ecocyc Extractor Changelog

This version is for extraction process with new Ecocyc release 26.5 for the RegulonDB 11.2 release.

## [2.0.1](https://github.com/regulondbunam/ecocyc-extractor/releases/tag/2.0.1) - 2023-02-24

### Added

- Test Module: This module checks functions works for debugging porposes.
- New Evidence Code generation, now is generated using the Evidence ID.
- New Evidence properties added.
  - type
  - crossEvidenceCodeRule
  - evidenceClass
  - evidenceCategory
  - evidenceApproach
  - noteWeb
- confidenceLevel property added.
  - The confidenceLevel property added in genes, products, promoters, regulatory complexes, regulatory continuants, regulatory interactions, segments, sigma factors, terminators, sites, transcription factors and transcription units.
- Symmetry TF property

### Changed

- The Evidence properties where added for future Ecocyc releases, these changes is to maintain parity with the MultigenomicModel
- Regulatory Interactions absoluteCenterPosition changed to relativeDistSitePromoter

### Deprecated

- Old Evidence Code generation, Code was generated using the Evidence name
- Removed an unnecessary print in the evidence extraction

### Fixed

- README:
  - Badges versions update and orthographics corrections.
  - Badges CHANGELOG link update.
- Snakefile: Commented code corrected.
- Some files has modifications in the import statements for testing porposes, it does not affect the code execution and will be implemented eventually in the rest of the files.
- Products crash fixed.
- TF SiteLength property extracted correctly.
- Restored staticmethod in Ontology.
