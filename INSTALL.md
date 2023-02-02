# RegulonDB Ecocyc Extractor Install

- ## Installation instructions

To use Ecocyc Extractor, a docker container with PathwayTools is required.

- Step 1
Download the [PathwayTools Docker](https://github.com/pablo-epl/pathway-tools-docker) :

```shell
$git clone https://github.com/pablo-epl/pathway-tools-docker
```

- Step 2

   Modify ```.env``` file with the current version of PathwayTools you need ```PT_VERSION="Client_Version"``` example:

```bash
PT_VERSION=25.0
```

- Step 3

   Download the [PathwayTools installer](https://bioinformatics.ai.sri.com/ptools/) this most be named ```pathway-tools-"Client_Version"-linux-64-tier1-install``` example:

```shell
pathway-tools-install/
├── pathway-tools-25.0-linux-64-tier1-install
└── pathway-tools_installer_here.md
```

- Step 4

   Build the Docker container:

```shell
$docker-compose build
```

- Step 5

   Start up the container:

```shell
$docker-compose up
```

6.Step 6

   Download the EcocycExtractor software at the directory you wish:

```shell
$git clone https://github.com/regulondbunam/ecocyc-extractor
```

- Step 7

   Now you can use the software, for more details checkout the [User Manual](docs/MU.md)

- **Dependencies**

  - [PathwayTools Docker](https://github.com/pablo-epl/pathway-tools-docker)
  - [PathwayTools installer](https://bioinformatics.ai.sri.com/ptools/)

- **Errors & Tips**
  - Be sure to start up the PathwayTools before run the program.

  - To see the arguments that the program supports use ```-h``` option

  ```shell
  $py ecocyc-extractor -h
  ```
