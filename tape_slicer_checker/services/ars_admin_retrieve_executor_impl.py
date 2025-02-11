import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List
import logging

from tape_slicer_checker.config.tape_slicer_checker_config import ArsAdminRetrieveConfig
from tape_slicer_checker.services.ars_admin_retrieve_executor import ArsAdminRetrieveExecutor
from tape_slicer_checker.services.cmd_parameters import CmdParameters

logger = logging.getLogger(__name__)

class ArsAdminRetrieveExecutorImpl(ArsAdminRetrieveExecutor):
    def __init__(
        self, 
        ars_admin_retriever_config: ArsAdminRetrieveConfig,
        output_dir: Path
    ):
        self._workers_no = ars_admin_retriever_config.workers_no
        self._output_dir = output_dir
        self._ondemand_instance = ars_admin_retriever_config.ondemand_instance
        self._ondemand_user = ars_admin_retriever_config.ondemand_user
        
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def _create_command(self, params: CmdParameters) -> list[str]:
        return [
            "arsadmin", "retrieve",
            "-I", self._ondemand_instance,
            "-u", self._ondemand_user,
            "-g", params.ag_name,
            "-n", params.node,
            params.file_name
        ]

    def _execute_command(self, params: CmdParameters) -> None:
        command = self._create_command(params)
        location = Path(self._output_dir / params.ag_name)
        location.mkdir(parents=True, exist_ok=True)
        joined_command = ' '.join(command)
        logger.debug(f"Executing : {joined_command}, from dir: {location}")
        
        try:
            subprocess.run(
                self._create_command(params),
                check=True,
                capture_output=True,
                cwd=location
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed: {joined_command}, from dir: {location}, error: {e}")

    def execute_commands(self, params_list: List[CmdParameters]) -> None:
        with ThreadPoolExecutor(max_workers=self._workers_no) as executor:
            executor.map(self._execute_command, params_list)