from abc import ABC, abstractmethod
from typing import List

from tape_slicer_checker.services.cmd_params_lookup_impl import CmdParameters


class ArsAdminRetrieveExecutor(ABC):
    @abstractmethod
    def execute_commands(self, params_list: List[CmdParameters]) -> None:
        pass