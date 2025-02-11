import logging
from pathlib import Path

from tape_slicer_checker.config.tape_slicer_checker_config import TapeSlicerCheckerConfig, load_config
from tape_slicer_checker.logging import logging_setup
from tape_slicer_checker.services.ars_admin_retrieve_executor_impl import ArsAdminRetrieveExecutorImpl
from tape_slicer_checker.services.checksum_verifier_impl import ChecksumVerifierImpl
from tape_slicer_checker.services.cmd_parameters import CmdParameters
from tape_slicer_checker.services.cmd_params_lookup_impl import CmdParamsLookupImpl
from tape_slicer_checker.services.remag_table_lookup_impl import RemagTableLookupImpl
from tape_slicer_checker.services.remnode_table_lookup_impl import RemnodeTableLookupImpl
from tape_slicer_checker.db2.db2_connection import DB2Connection

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    config: TapeSlicerCheckerConfig = load_config('./tape_slicer_checker/resources/tape_slicer_checker_config.yaml')

    logging_setup.setup_logging(config.logging_config)
    logger.info("tape_slicer_checker starting...")
    
    db2_connection = DB2Connection(config.db_config)
    remag_table_lookup = RemagTableLookupImpl(db2_connection)
    remnode_table_lookup = RemnodeTableLookupImpl(db2_connection)
    cmd_params_lookup = CmdParamsLookupImpl(remag_table_lookup, remnode_table_lookup)
    ars_admin_retrieve_executor = ArsAdminRetrieveExecutorImpl(config.ars_admin_retrieve_config)
    checksum_verifier = ChecksumVerifierImpl()
    
    path_objects: list[tuple[Path, CmdParameters]] = cmd_params_lookup.process_directory(config.checker_config.source_dir)
    objects: list[CmdParameters] = [elem[1] for elem in path_objects]
    logger.info(f"Arsadmin parameters fetched from db for {len(path_objects)} objects from {config.checker_config.source_dir}")
    
    ars_admin_retrieve_executor.execute_commands(objects)
    logger.info("Arsadmin retrieve command executed.")
    
    file_pairs: list[tuple[Path, Path]] = [
        (elem[0], config.ars_admin_retrieve_config.output_dir / elem[1].ag_name / elem[1].file_name) 
        for elem in path_objects
    ]
    
    failed_verification: list[tuple[Path, Path]] = checksum_verifier.verify(file_pairs)
    logger.info("Files verification finished")
    
    if failed_verification:
        logger.error(f"Number of failed pairs: {len(failed_verification)}")
    else:
        logger.info("All pairs are correct.")
    
    
