import logging
from pathlib import Path
from typing import List, Tuple
import filecmp
from tape_slicer_checker.services.checksum_verifier import ChecksumVerifier

logger = logging.getLogger(__name__)

class ChecksumVerifierImpl(ChecksumVerifier):
    def verify(self, file_pairs: List[Tuple[Path, Path]]) -> list[tuple[Path, Path]]:
        failed_pairs: list[tuple[Path, Path]] = []
        
        for file1, file2 in file_pairs:
            try:
                if not filecmp.cmp(file1, file2, shallow=False):
                    logger.error(f"FAILED: {file1} {file2}")
                    failed_pairs.append((file1, file2))
                else:
                    logger.info(f"OK: {file1} {file2}")
            except Exception as e:
                logger.error(f"Failed comparison {file1}  {file2}: {str(e)}")
                failed_pairs.append((file1, file2))
        
        return failed_pairs