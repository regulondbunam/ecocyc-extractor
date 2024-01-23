configfile: "config/config.json"

ptools_config = config["ptools_config"]
ecocyc_extractor_config  = config["ecocyc_extractor_config"]
schema_loader_config = config["schema_loader_config"]
validation_config = config["validation_config"]
create_identifiers_config = config["create_identifiers_config"]
replace_identifiers_config = config["replace_identifiers_config"]
revalidation_config = config["revalidation_config"]
data_upload_config = config["data_upload_config"]


rule ecocyc_extractor_workflow:
    params:
        compose_file = {ptools_config["compose_file"]}, # -f
        dotenv_file = {ptools_config["dotenv_file"]}, # --env-file
    input:
        #"logs/ptools_docker_log/ptools_docker_log.log",
        #"logs/ecocyc_extractor_log/ecocyc_extractor_log.log",
        "logs/schema_loader_log/schema_loader_log.log",
        "logs/validation_log/validation_log.log",
        "logs/create_identifiers_log/create_identifiers_log.log",
        "logs/replace_identifiers_log/replace_identifiers_log.log",
        "logs/re_validation_log/validation_log.log",
        "logs/data_uploader_log/data_uploader_log.log"
    log: 
        "logs/ecocyc_extractor_log.log"
    run:
        shell('python ../log_cleaner/log_cleaner.py'),
        #shell("docker-compose -f {params.compose_file} --env-file {params.dotenv_file} stop")

rule ptools_docker:
    params:
        compose_file = {ptools_config["compose_file"]}, # -f
        dotenv_file = {ptools_config["dotenv_file"]} # --env-file
    log:
        "logs/ptools_docker_log/ptools_docker_log.log"
    priority: 11
    run:
        shell("docker-compose -f {params.compose_file} --env-file {params.dotenv_file} build")
        shell("docker-compose -f {params.compose_file} --env-file {params.dotenv_file} up -d")
        shell('echo "Please Wait for PTools Startup"')
        shell("sleep 10s")
        
rule ecocyc_extractor:
    params:
        main_path = ecocyc_extractor_config["main_path"],
        output_dir = ecocyc_extractor_config["raw_data"],
        log_dir = ecocyc_extractor_config["log_dir"]
    output:
        log = "logs/ecocyc_extractor_log/ecocyc_extractor_log.log"
    log:
        "logs/ecocyc_extractor_log/ecocyc_extractor_log.log"
    conda:
        "envs/ecocyc_dependencies.yaml"
    priority: 10
    shell:
        "python {params.main_path} -a -out {params.output_dir} -l {params.log_dir}"


rule schema_loader:
    params:
        main_path = schema_loader_config["main_path"],
        db = config["db"],
        url = config["url"],
        schemas = schema_loader_config["schemas"],
        log = schema_loader_config["log_dir"]
    log:
        "logs/schema_loader_log/schema_loader_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 9
    shell:
        "python {params.main_path} -db {params.db} -u {params.url} -s {params.schemas} -l {params.log} -d"


rule data_validator:
    params:
        main_path = validation_config["main_path"],
        data = validation_config["raw_data"],
        schemas = validation_config["schemas"],
        valid_data = validation_config["verified_data"],
        invalid_data = validation_config["invalid_data"],
        log = validation_config["log_dir"]
    log:
        "logs/validation_log/validation_log.log"
    conda:
        "envs/py_down_grade.yaml"
    priority: 8
    shell:
        "python {params.main_path} -i {params.data} -s {params.schemas} -v {params.valid_data} -iv {params.invalid_data} -l {params.log} -sp"


rule create_identifiers:
    params:
        main_path = create_identifiers_config["main_path"],
        valid_data = create_identifiers_config["verified_data"],
        log = create_identifiers_config["log_dir"],
        db = config["db"],
        url = config["url"],
        organism = config["organism"],
        version = config["version"],
        source = config["source"],
        source_version = config["source_version"],
    log:
        "logs/create_identifiers_log/create_identifiers_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 7
    shell:
        'python3 {params.main_path} -u {params.url} -i {params.valid_data} -org {params.organism} -s {params.source} -sv {params.source_version} -v {params.version} -db "{params.db}" -l {params.log}'


rule replace_identifiers:
    params:
        main_path = replace_identifiers_config["main_path"],
        valid_data = replace_identifiers_config["verified_data"],
        replaced_ids = replace_identifiers_config["persistent_ids"],
        log = replace_identifiers_config["log_dir"],
        organism = config["organism"],
        version = config["version"],
        db = config["db"],
        url = config["url"],
    log:
        "logs/replace_identifiers_log/replace_identifiers_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 6
    shell:
        "python {params.main_path} -org {params.organism} -i {params.valid_data} -o {params.replaced_ids} -u {params.url} -v {params.version} -db {params.db} -l {params.log}"


rule re_validate_data:
    params:
        main_path = revalidation_config["main_path"],
        data = revalidation_config["persistent_ids"],
        schemas = revalidation_config["schemas"],
        valid_data = revalidation_config["verified_persistent_ids"],
        invalid_data = revalidation_config["invalid_data"],
        log = revalidation_config["log_dir"]
    log:
        "logs/re_validation_log/validation_log.log"
    conda:
        "envs/py_down_grade.yaml"
    priority: 5
    shell:
        "python {params.main_path} -i {params.data} -s {params.schemas} -v {params.valid_data} -iv {params.invalid_data} -l {params.log}"


rule data_uploader:
    params:
        main_path = data_upload_config["main_path"],
        valid_data = data_upload_config["verified_persistent_ids"],
        log = data_upload_config["log_dir"],
        db = config["db"],
        url = config["url"]
    log:
        "logs/data_uploader_log/data_uploader_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 4
    shell:
        "python {params.main_path} -i {params.valid_data} -u {params.url} -db {params.db} -l {params.log}"
