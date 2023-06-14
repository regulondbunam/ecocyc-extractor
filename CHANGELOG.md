# Ecocyc Extractor Changelog

This version is for extraction process with new Ecocyc release 27.0 for the RegulonDB 12.0 release.

## [2.0.3](https://github.com/regulondbunam/ecocyc-extractor/releases/tag/2.0.3) - 2023-06-14

### Added

- New RegulatoryIteractions property 'regulationClass'.

### Changed

- Now when a new conformation will be added it's checked if this is not a TF.

### Deprecated

- Old Evidence Code generation, Code was generated using the Evidence name
- Removed an unnecessary print in the evidence extraction

### Fixed

- Without changes.

### To Fix

- There's a possibility to modify the regulationClass property format.
