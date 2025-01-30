from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

@dataclass
class LoggingConfig:
    log_dir: Path
    log_label: str

@dataclass
class DbConfig:
    database: str
    user: str
    password: str
    
@dataclass
class CheckerConfig:
    source_dir: Path
    
@dataclass
class ArsAdminRetrieveConfig:
    workers_no: int
    output_dir: Path
    ondemand_instance: str
    ondemand_user: str

@dataclass
class TapeSlicerCheckerConfig:
    logging_config: LoggingConfig
    db_config: DbConfig
    checker_config: CheckerConfig
    ars_admin_retrieve_config: ArsAdminRetrieveConfig


def load_config(config_path: Optional[str] = None) -> TapeSlicerCheckerConfig:
    if config_path is None:
        config_path = str(Path(__file__).parent / 'resources' / 'tape_slicer_checker_config.yaml')

    with open(config_path) as f:
        yaml_config = yaml.safe_load(f)

    return TapeSlicerCheckerConfig(
        logging_config=LoggingConfig(
            log_dir=Path(yaml_config['logging_config']['log_dir']),
            log_label=yaml_config['logging_config']['log_label'],
        ),
        db_config=DbConfig(
          database=yaml_config['db_config']['database'],
          user=yaml_config['db_config']['user'],
          password=yaml_config['db_config']['password']
        ),
        checker_config=CheckerConfig(
            source_dir=Path(yaml_config['checker_config']['source_dir'])
        ),
        ars_admin_retrieve_config=ArsAdminRetrieveConfig(
            workers_no=yaml_config['arsadmin_retriever_config']['workers_no'],
            output_dir=Path(yaml_config['arsadmin_retriever_config']['output_dir']),
            ondemand_instance=yaml_config['arsadmin_retriever_config']['ondemand_instance'],
            ondemand_user=yaml_config['arsadmin_retriever_config']['ondemand_user']
        )
    )