from dataclasses import dataclass


@dataclass
class CmdParameters:
    ag_name: str
    node: str
    file_name: str