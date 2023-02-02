# Ecocyc Extractor Changelog

This version solves the changes on Ecocyc 24.5 release.

## [0.1.1](https://github.com/regulondbunam/ecocyc-extractor/releases/tag/0.1.1) - 2021-08-25

### Added
- Added externalCrossReferences property to all classes: These contain ObjectID which is your original Ecocyc class ID and a reference to Ecocyc in new cases that were not included in the extraction.
- Added distanceToGene property to Promoters class.
- In the Genes collection, the fragments property added the *name* and *id* properties.
- The absolutePosition property was added to the RI's extraction.
- RI's regulatedEntity property can now contain Genes.
- New RIs Protein-Mediated-Translation-Regulation were added.
- Now regulationType, in RI and Sites, has three types ["Transcription", "RNA-Regulation", "Protein-Regulation"].
- AccessoryProteins property added to RI.

### Changed
- RI's regulatedEntities property was changed to regulatedEntity, now it is an object, not an array.
- TU's property promoters_ids was changed to promoters_id, now it is a string not an array.
- The Segments class responsible for containing the information of the EcoCyc DNA-Segments and mRNA-Segments classes has been added.
- The TranscriptionFactorsRegulatorySites class was updated to regulatorySites.
- The type property in RI 'and Sites was updated to mechanism.
- In TF collection the  TF Complexes citations are extracted and the regulatoryComplex citations are eliminated.
- Sites' sequence now are every time in forward mode.

### Deprecated
- Added new collection called crypticProphages, this collection has been deprecated.

### Fixed
- Fixed a problem with the function that returned sequence in the extraction of Sites
- Fixed duplicated ciotations in TF collection. Two lists were  generated and joined but it was not verified that citations were not  repeated.
