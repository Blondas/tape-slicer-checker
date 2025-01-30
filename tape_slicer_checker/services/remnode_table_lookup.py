from abc import ABC, abstractmethod

class RemnodeTableLookup(ABC):
    @abstractmethod
    def nid(self, sid: int) -> str:
        pass