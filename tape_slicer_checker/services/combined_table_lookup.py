from abc import ABC, abstractmethod
from typing import Tuple


class CombinedTableLookup(ABC):
    @abstractmethod
    def agname_nid(self, agid_name: str) -> Tuple[str, int]:
        pass