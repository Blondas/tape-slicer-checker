from abc import ABC, abstractmethod

from tape_slicer_checker.services.cmd_params_lookup_impl import CmdParameters

class CmdParamsLookup(ABC):
    @abstractmethod
    def get_params(self, object_file_name: str) -> CmdParameters:
        pass