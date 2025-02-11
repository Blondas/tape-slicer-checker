
from pathlib import Path
from typing import List, Tuple
import logging

from tape_slicer_checker.services.cmd_parameters import CmdParameters
from tape_slicer_checker.services.cmd_params_lookup import CmdParamsLookup
from tape_slicer_checker.services.combined_table_lookup import CombinedTableLookup
logger = logging.getLogger(__name__)
    
class CmdParamsLookupImpl(CmdParamsLookup):
    def __init__(
        self,
        combined_table_lookup: CombinedTableLookup,
    ) -> None:
        self._combined_table_lookup = combined_table_lookup
    
    def get_params(self, file_name: str) -> CmdParameters:
        parts = file_name.split(".")
        
        if len(parts) == 2:
            agid_name, load_id = parts
            ag_name, nid = self._combined_table_lookup.agname_nid(agid_name)
            
            return CmdParameters(ag_name, f'{nid}-0', load_id[1:])
            
        elif len(parts) == 3:
            agid_name, load_id, load_id_suffix = parts
            ag_name, nid = self._combined_table_lookup.agname_nid(agid_name)
            return CmdParameters(ag_name, f'{nid}-0', f'{load_id[1:]}{load_id_suffix}')
        else :
            raise ValueError(f"File name must contain either 1 or 2 dots, file name: {file_name}")
        
    def process_directory(self, src_dir: Path) -> List[Tuple[Path, CmdParameters]]:
        if not src_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {src_dir}")
        if not src_dir.is_dir():
            raise ValueError(f"Path of source directory is not a directory: {src_dir}")

        results: List[Tuple[Path, CmdParameters]] = []

        for file_path in src_dir.iterdir():
            if file_path.is_file():  # Process only files, skip directories
                try:
                    params: CmdParameters = self.get_params(file_path.name)
                    results.append((file_path, params))
                except ValueError as e:
                    logging.warning(f"Skipping file {file_path}: {str(e)}")
                except Exception as e:
                    logging.error(f"Error processing file {file_path}: {str(e)}")

        return results