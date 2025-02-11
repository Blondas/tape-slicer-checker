import logging
from pathlib import Path
import argparse

from tape_slicer_checker.logging import logging_setup
from tape_slicer_checker.config.tape_slicer_checker_config import TapeSlicerCheckerConfig, load_config
from tape_slicer_checker.services.ars_admin_retrieve_executor_impl import ArsAdminRetrieveExecutorImpl
from tape_slicer_checker.services.checksum_verifier_impl import ChecksumVerifierImpl
from tape_slicer_checker.services.cmd_parameters import CmdParameters
from tape_slicer_checker.services.cmd_params_lookup_impl import CmdParamsLookupImpl
from tape_slicer_checker.services.combined_table_lookup_impl import CombinedTableLookupImpl
from tape_slicer_checker.db2.db2_connection import DB2Connection
from tape_slicer_checker.utils.delete_path import delete_path

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='Tape Slicer Checker')
    parser.add_argument('--input-dir', type=Path, required=True, help='Input directory')
    parser.add_argument('--tape-name', type=str, required=True, help='Tape name')
    parser.add_argument('--output-dir', type=Path, required=True, help='Output directory')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    config: TapeSlicerCheckerConfig = load_config('./tape_slicer_checker/resources/tape_slicer_checker_config.yaml')
    logging_setup.setup_logging(args.output_dir)
    logger.info("tape_slicer_checker starting...")

    db2_connection = DB2Connection(config.db_config)
    combined_table_lookup = CombinedTableLookupImpl(db2_connection, args.tape_name)
    cmd_params_lookup = CmdParamsLookupImpl(combined_table_lookup)
    ars_admin_retrieve_executor = ArsAdminRetrieveExecutorImpl(config.ars_admin_retrieve_config, args.output_dir)
    checksum_verifier = ChecksumVerifierImpl()

    path_objects: list[tuple[Path, CmdParameters]] = cmd_params_lookup.process_directory(args.input_dir)
    objects: list[CmdParameters] = [elem[1] for elem in path_objects]
    logger.info(f"Arsadmin parameters fetched from db for {len(path_objects)} objects from {args.input_dir}")

    ars_admin_retrieve_executor.execute_commands(objects)
    logger.info("Arsadmin retrieve command executed.")

    file_pairs: list[tuple[Path, Path]] = [
        (elem[0], args.output_dir / elem[1].ag_name / elem[1].file_name) 
        for elem in path_objects
    ]

    failed_verification: list[tuple[Path, Path]] = checksum_verifier.verify(file_pairs)
    logger.info("Files verification finished")

    if failed_verification:
        logger.error(f"Number of failed pairs: {len(failed_verification)}")
    else:
        delete_path(args.output_dir)
        logger.info("All pairs are correct. Output directory deleted")
