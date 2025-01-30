from typing import Dict, Tuple
import logging

from tape_slicer_checker.db2.db2_connection import DB2Connection
from tape_slicer_checker.services.remag_table_lookup import RemagTableLookup

logger = logging.getLogger(__name__)

class RemagTableLookupImpl(RemagTableLookup):
    def __init__(
        self,
        db2_connection: DB2Connection
    ) -> None:
        self._db2_connection = db2_connection
        self._dict: Dict[str, Tuple[str, int]] = self._fetch()

    def _fetch(self) -> Dict[str, Tuple[str, int]]:
        with self._db2_connection.connect() as connection:
            query: str = "SELECT distinct(agid_name), name, sid FROM remag"
            cursor = connection.cursor()
            cursor.execute(query)
            return {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
        
    def agname_sid(self, agid_name: str) -> Tuple[str, int]:
        try:
            return self._dict[agid_name]
        except KeyError:
            logger.warning(f"No such ag_name in remag table for agid_name: {agid_name}")