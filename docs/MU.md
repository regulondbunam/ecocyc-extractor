# User Manual Ecocyc Extractor

## Introduction

The Snakemake script for the Ecocyc Extractor data extraction transform and load process was thought to make uploading data to RegulonDB Multigenomic faster and more controlled, due to the modular nature of Snakemake allows the upload process to be carried out from any computer that meets the execution requirements but without the need to configure its _Python_ environment for each of the data load modules.

## Snakefile run

To run the Snakefile script you must follow the following steps.

- Run the complete script:

```shell
$snakemake --use-conda -j1
```

<br>The `-s` parameter is the name of the Snakefile script.
<br>The option `--cores` or `-j` (`-j1` for example) indicates how many cores of the computer will be used to process the script, it is recommended to indicate them to avoid problems when executing.
<br>The `--use-conda` option is used to indicate that the _conda_ environment is used to download the necessary modules and create sandboxes.

- Run the script as a test:

```shell
$snakemake -j1 --use-conda -n
```

<br>The `-n` parameter indicates that a clean test execution will be run showing the jobs to be executed or if there is a problem with the script.

- Execute only one rule:

```shell
$snakemake -j1 --use-conda -R [my_rule]
```

<br>The parameter `-R` indicates the name of the _rule_ that you want to execute, you can put several and they will be executed in the order given.

- Run the script forcibly:

```shell
$snakemake -j1 --use-conda -f
```

<br>The `-f` parameter is to perform a forced execution, in case the output files have already been generated to execute the script or a single rule.

- Run script and generate a report:

```shell
$snakemake -j1 --use-conda -report
```

<br>The `-report` parameter is used to generate a report, in html format, of the execution of the script with the memory data and the _log_ in general in a graphical presentation.

## ecocyc_extractor module

<br>The ecocyc_extractor data extraction module has console parameter handling, for a better use of it you can follow these recommendations (only for isolated execution of the module outside the script):

- General arguments, this arguments set some paths to directories or files necessary in the execution and other params nedded.
  - `"-out", "--output", "Path where the json files of the process will be stored."`
  - `" -l "," --log ","Path where the log of the process will be stored."`
  - `"-org", "--organism", "Organism whose information is been downloaded."`

- Collection arguments, this arguments indicates which collections will be processed.
  - `"-a", "--all", "Sets the extractor to download all the available classes, ignoring all arguments except --allpb and --alldb"`
  - `"-alldb", "--all-external-databases", "Sets the extractor to download all the External Databases and not only the ones registered in the downloaded objects"`
  - `"-allpb", "--all-publications", "Sets the extractor to download all the Publications and not only the ones registered in the downloaded objects"`
  - `"-pb", "--publications", "Sets the extractor to download Publications"`
  - `"-extdb", "--external-databases", "Sets the extractor to download External Databases"`
  - `"-ev", "--evidences", "Sets the extractor to download Evidences"`
  - `"-mft", "--multifun-terms", "Sets the extractor to download Ontologies' Terms"`
  - `"-mot", "--multifun-ontology", "Sets the extractor to download Ontologies(MultiFun, GO Terms)"`
  - `"-gotm", "--got-terms", "Sets the extractor to download Ontologies' Terms"`
  - `"-got", "--gene-ontology", "Sets the extractor to download Ontologies(MultiFun, GO Terms)"`
  - `"-ot", "--ontologies", "Sets the extractor to download Ontologies(MultiFun, GO Terms)"`
  - `"-rc", "--regulatory-continuants", "Sets the extractor to download Regulatory Continuants"`
  - `"-rcplx", "--regulatory-complexes", "Sets the extractor to download Regulatory Complexes"`
  - `"-st", "--sites", "Sets the extractor to download Sites"`
  - `"-ri", "--regulatory-interactions", "Sets the extractor to download Regulatory Interactions"`
  - `"-sf", "--sigma-factors", "Sets the extractor to download Sigma Factors"`
  - `"-tf", "--transcription-factors", "Sets the extractor to download Transcription Factors"`
  - `"-sg", "--segments", "Sets the extractor to download Segments"`
  - `"-pph", "--prophages", "Sets the extractor to download Cryptic Prophages"`
  - `"-pm", "--promoters", "Sets the extractor to download Promoters"`
  - `"-tm", "--terminators", "Sets the extractor to download Terminators"`
  - `"-op", "--operons", "Sets the extractor to download Operons"`
  - `"-tu", "--transcription-units", "Sets the extractor to download Transcription Units"`
  - `"-mt", "--motifs", "Sets the extractor to download Motifs"`
  - `"-pd", "--products", "Sets the extractor to download Products"`
  - `"-gcpc", "--growth-condition-phrase-catalog", "Sets the extractor to download Growth Condition Phrase Catalog"`
  - `"-gn", "--genes", "Sets the extractor to download Genes"`

<br>For this module the library [`PythonCyc`]( https://github.com/regulondbunam/PythonCyc) is needed, this one that allows to connect to the Ecocyc's API [PathwayTools 26.0](http://bioinformatics.ai.sri.com/ptools/) and then access to the Ecocyc DataBase , if the module is executed with the Snakefile script it is not necessary to install it on your computer directly, you only need to indicate in the file `envs/ecocyc_dependencies.yaml` the name and version of the library.

```yaml
channels:
  - bioconda
  - conda-forge
  - local
dependencies:
  - python = 3.10
  - pip
  - pip:
      - ../../../libs/PythonCyc-master/
```

Also check the other enviroments files

`envs/db_dependencies.yaml`

```yaml
channels:
  - bioconda
  - conda-forge
  - local
dependencies:
  - python = 3.10
  - mongoengine
  - pymongo = 3.12.1
  - dnspython
  - pip
  - pip:
      - ../../../libs/identifiers/
```

`envs/py_down_grade.yaml`

```yaml
channels:
  - bioconda
  - conda-forge
  - local
dependencies:
  channels:
 - bioconda
 - conda-forge
dependencies:
 - python = 2.7
 - jsonschema
```

## Definitions, acronyms and abbreviations

- **[Snakemake](https://snakemake.readthedocs.io/en/stable/)** - The Snakemake workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language.
- **[PythonCyc]( https://github.com/regulondbunam/PythonCyc)** -The PythonCyc module provides a Python 3.5+ interface to a Pathway Tools application running either locally or remotely. This module has been designed to work on the three platforms supported by Pathway Tools: Linux, Mac OS X, and Windows. Pathway Tools version 18.5 or above is needed to use this module.

## Help and Support

If you have a problem or suggestion of any kind related to what is described in this manual, you can send an email to: [regusoft@ccg.unam.mx](mailto:regusoft@ccg.unam.mx)

The documents mentioned as reference in this manual may be requested through the aforementioned address.

## Bibliographic references

**Websites**

- Website title: Snakemake
  - Web link: [https://snakemake.readthedocs.io/en/stable/](https://snakemake.readthedocs.io/en/stable/)

- Website title: PythonCyc
  - Web link: [https://bioinformatics.ai.sri.com/ptools/pythoncyc](https://bioinformatics.ai.sri.com/ptools/pythoncyc.html)

- Website title: PathwayTools
  - Web link: [https://bioinformatics.ai.sri.com/ptools/](https://bioinformatics.ai.sri.com/ptools/)
