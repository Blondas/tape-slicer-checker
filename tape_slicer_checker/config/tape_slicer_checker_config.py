from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

@dataclass
class DbConfig:
    database: str
    user: str
    password: str
    
@dataclass
class ArsAdminRetrieveConfig:
    workers_no: int
    ondemand_instance: str
    ondemand_user: str

@dataclass
class TapeSlicerCheckerConfig:
    db_config: DbConfig
    ars_admin_retrieve_config: ArsAdminRetrieveConfig


def load_config(config_path: Optional[str] = None) -> TapeSlicerCheckerConfig:
    if config_path is None:
        config_path = str(Path(__file__).parent / 'resources' / 'tape_slicer_checker_config.yaml')

    with open(config_path) as f:
        yaml_config = yaml.safe_load(f)

    return TapeSlicerCheckerConfig(
        db_config=DbConfig(
          database=yaml_config['db_config']['database'],
          user=yaml_config['db_config']['user'],
          password=yaml_config['db_config']['password']
        ),
        ars_admin_retrieve_config=ArsAdminRetrieveConfig(
            workers_no=yaml_config['arsadmin_retriever_config']['workers_no'],
            ondemand_instance=yaml_config['arsadmin_retriever_config']['ondemand_instance'],
            ondemand_user=yaml_config['arsadmin_retriever_config']['ondemand_user']
        )
    )