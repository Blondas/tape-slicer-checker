from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple

class ChecksumVerifier(ABC):
    @abstractmethod
    def verify(self, file_pairs: List[Tuple[Path, Path]]) -> list[tuple[Path, Path]]:
        pass