import logging

from tape_slicer_checker.config.tape_slicer_checker_config import TapeSlicerCheckerConfig, load_config
from tape_slicer_checker.logging import logging_setup

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    config: TapeSlicerCheckerConfig = load_config('./tape_slicer_checker/resources/tape_slicer_checker_config.yaml')

    logging_setup.setup_logging(config.logging_config)
    logger.info("tape_slicer_checker starting...")