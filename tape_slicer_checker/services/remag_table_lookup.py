from abc import ABC, abstractmethod
from typing import Tuple


class RemagTableLookup(ABC):
    @abstractmethod
    def agname_sid(self, agid_name: str) -> Tuple[str, int]:
        pass