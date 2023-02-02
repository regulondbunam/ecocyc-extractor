<h1 align="center"> RegulonDB Ecocyc Extractor </h1>
<p align="center" >
  <img alt="RegulonDB Logo" style="width:50%;height:25%;" src="https://drive.google.com/uc?export=view&id=1BtKqNvtchMidDMUSyeJZPCnfMb-saaYm"></img>
</p>

![Licence](https://img.shields.io/badge/licence-MIT-brightgreen?style=plastic)
![RegulonDBVersion](https://img.shields.io/badge/RegulonDB_version-11.1-blue?style=plastic&link=https://regulondb.ccg.unam.mx/)
![EcocycVersion](https://img.shields.io/badge/last_Ecocyc_version_tested-26.0-red?style=plastic&link=https://ecocyc.org/)
![Status](https://img.shields.io/badge/status-in_development-yellowgreen?style=plastic)

This [software](https://lucid.app/folder/invitations/accept/813e6281-f3fb-4a08-967a-251e1e5af6b7) has the function of extracting the information from the Ecocyc database and transforming it for use in RegulonDB with respect to the [Multigenomic Model](https://app.lucidchart.com/lucidchart/invitations/accept/0056e953-5ccb-439d-9411-afcb9c875953)

# Motivation

RegulonDB is undergoing a reengineering process, using open access technologies. Now instead of using Oracle as the database administrator, MongoDB will be used, access to the data will be through web services using GraphQL and Python for data processing.

RegulonDB is the primary database on transcriptional regulation in Escherichia coli K-12 containing knowledge manually curated from original scientific publications, complemented with high throughput datasets and comprehensive computational predictions.
This software was made to extract all the necessary data from Ecocyc.

# System requirements

- Software:
  - [Python 3.10](https://www.python.org/) or above
  - [RegulonDB PythonCyc Fork](https://github.com/regulondbunam/PythonCyc)
  - [PathwayTools Docker](https://github.com/pablo-epl/pathway-tools-docker)
  - [PathwayTools 26.0](http://bioinformatics.ai.sri.com/ptools/)
- Hardware:
  - RAM: 8 GB (recommended)
  
  - Storage: 5 GB
  
# Install

[Install guide](INSTALL.md)

# Quick start

```shell
python ecocyc-extractor/ -a
```

# Manuals

- [User Manual](docs/MU.md)
- [Operation Manual](docs/MO.md)
- [Maintenance Manual](docs/MM.md)

# Project website

[RegulonDB WebSite](https://regulondb.ccg.unam.mx/)

# License

RegulonDB Ecocyc Extractor is [MIT licensed](LICENSE).

# Contributors

Check RegulonDB Ecocyc Extractor [contributors](CONTRIBUTORS.md).

# Support contact information

[Support contact](http://regulondb.ccg.unam.mx/menu/about_regulondb/contact_us/index.jsp)

# Software quality checklist

**Accessibility**

- [x] Version control system

**Documentation**

- [x] README file

**Learnability**

- [x] Quick start

**Buildability**

- [x] INSTALL file

**Identity**

- [x] Website

**Copyright & Licensing**

- [x] LICENSE file

**Portability**

- [x] Multiple platforms

**Supportability**

- [x] E-mail address
- [x] Issue tracker

**Analysability**

- [x] Source code structured
- [x] Coding standards - [Google style guides](http://google.github.io/styleguide/) [Python style guide](https://pep8.org/#pep-8-%E2%80%94-the-style-guide-for-python-code)

**Changeability**

- [x] CONTRIBUTING file
- [x] Code of Conduct file
- [x] Code changes, and their authorship, publicly visible

**Reusability**

- [x] Source code set up in a modular fashion

**Security & Privacy**

- [x] Passwords must never be stored in unhashed form
