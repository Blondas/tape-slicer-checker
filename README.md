# Tape Slicer Checker

## Overview

The `tape_slicer_checker` is a tool designed to verify object cut by tape-slicer and retrieved files from a tape storage system (using `arsadmin retrieve`). It uses command-line arguments to specify input and output directories, as well as the tape name.

## Requirements

- Python 3.9 or higher
- virtual environment: `source /ars/home/lib/py3/bin/activate`

## Configuration

The configuration file `tape_slicer_checker_config.yaml` should be placed in the `tape_slicer_checker/resources` directory. This file contains the necessary configurations for the tool, including database and logging settings.

Example configuration (`tape_slicer_checker/resources/tape_slicer_checker_config.yaml`):
```yaml
db_config:
  host: "your_db_host"
  port: 50000
  user: "your_db_user"
  password: "your_db_password"
  database: "your_db_name"

ars_admin_retrieve_config:
  workers_no: 4
  ondemand_instance: "your_instance"
  ondemand_user: "your_user"
```

## Usage

To run the tape_slicer_checker, use the following command:
`python -m tape_slicer_checker --input-dir <input_directory> --tape-name <tape_name> --output-dir <output_directory>`

### Command-Line Arguments
--input-dir: The directory containing the input files.
--tape-name: The name of the tape.
--output-dir: The directory where the output files will be stored.

### Example
`python -m tape_slicer_checker --input-dir /path/to/input --tape-name TAPENAME --output-dir /path/to/output`

## Logging
The tool logs its activities to both the console and a log file. The log file is created in the specified output directory with a timestamp.  

## Cleaning Up
If all file pairs are verified successfully, the output directory will be deleted automatically.
