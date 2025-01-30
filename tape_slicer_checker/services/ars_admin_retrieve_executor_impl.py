import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import List
import logging

from tape_slicer_checker.config.tape_slicer_checker_config import ArsAdminRetrieveConfig
from tape_slicer_checker.services.ars_admin_retrieve_executor import ArsAdminRetrieveExecutor
from tape_slicer_checker.services.cmd_params_lookup_impl import CmdParameters

logger = logging.getLogger(__name__)

class ArsAdminRetrieveExecutorImpl(ArsAdminRetrieveExecutor):
    def __init__(
        self, 
        ars_admin_retriever_config: ArsAdminRetrieveConfig
    ):
        self._workers_no = ars_admin_retriever_config.workers_no
        self._output_dir = ars_admin_retriever_config.output_dir
        self._ondemand_instance = ars_admin_retriever_config.ondemand_instance
        self._ondemand_user = ars_admin_retriever_config.ondemand_user

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
        try:
            subprocess.run(
                self._create_command(params),
                check=True,
                capture_output=True,
                cwd=self._output_dir
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed for {params}: {e.stderr.decode()}")

    def execute_commands(self, params_list: List[CmdParameters]) -> None:
        with ThreadPoolExecutor(max_workers=self._workers_no) as executor:
            executor.map(self._execute_command, params_list)