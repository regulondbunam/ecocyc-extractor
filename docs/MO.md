# Operation Manual Ecocyc Extractor

## Introduction to the system

The Snakemake script for the Ecocyc Extractor data extraction transform and load process was thought to make uploading data to RegulonDB Multigenomic faster and more controlled, due to the modular nature of Snakemake allows the upload process to be carried out from any computer that meets the execution requirements but without the need to configure its _Python_ environment for each of the data load modules.

## Hardware Recommendations

- RAM: 8 GB
- Storage: 500 MB

## Software Requirements

- [Python 3.10](https://www.python.org/) or above
- [RegulonDB PythonCyc Fork](https://github.com/regulondbunam/PythonCyc)
- [PathwayTools Docker](https://github.com/pablo-epl/pathway-tools-docker)
- [PathwayTools 26.0](http://bioinformatics.ai.sri.com/ptools/)
- Operating System Linux/Unix (recommended)

## Installation Instructions

It is not necessary to do an installation, but it is necessary to place all the modules of the process with the directory structure of the diagram [Directory structure](../docs/diagrams/RegulonDBProyectsDirsTemplates.png) so that you have a better control from the Snakefile.

## Common problems

There can be a desicronization of _Rules_ problem, those are that control the execution of modules in order, if a module is executed before than expected it may have problems executing the next one since it depends on the files that the previous one generates.
It's recommended in the **_rule:_** to put a parameter **_priority:_** so that they are executed in order, keep in mind that the priority is higher the higher the value of the number that is specified.

```python
rule ecocyc_extractor:
 priority: 10
```

## Definitions, acronyms and abbreviations

- **[Snakemake](https://snakemake.readthedocs.io/en/stable/)** - The Snakemake workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language.
- **[PythonCyc]( https://github.com/regulondbunam/PythonCyc)** -The PythonCyc module provides a Python 3.5+ interface to a Pathway Tools application running either locally or remotely. This module has been designed to work on the three platforms supported by Pathway Tools: Linux, Mac OS X, and Windows. Pathway Tools version 18.5 or above is needed to use this module.

## Help and Support

If you have a problem or suggestion of any kind related to what is described in this manual, you can send an email to: [regusoft@ccg.unam.mx](mailto:regusoft@ccg.unam.mx)

The documents mentioned as reference in this manual may be requested through the aforementioned address.

## Bibliographic references

- Website title: Snakemake
  - Web link: [https://snakemake.readthedocs.io/en/stable/](https://snakemake.readthedocs.io/en/stable/)

- Website title: PythonCyc
  - Web link: [https://bioinformatics.ai.sri.com/ptools/pythoncyc](https://bioinformatics.ai.sri.com/ptools/pythoncyc.html)

- Website title: PathwayTools
  - Web link: [https://bioinformatics.ai.sri.com/ptools/](https://bioinformatics.ai.sri.com/ptools/)
