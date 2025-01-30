from typing import Dict

from tape_slicer_checker.db2.db2_connection import DB2Connection
from tape_slicer_checker.services.remnode_table_lookup import RemnodeTableLookup


class RemnodeTableLookupImpl(RemnodeTableLookup):
    def __init__(
        self,
        db2_connection: DB2Connection
    ) -> None:
        self._db2_connection = db2_connection
        self._dict: Dict[int, int] = self._fetch()

    def _fetch(self) -> Dict[int, int]:
        with self._db2_connection.connect() as connection:
            query: str = "SELECT sid, nid from remnode"
            cursor = connection.cursor()
            cursor.execute(query)
            return dict(cursor.fetchall())

    def nid(self, sid: int) -> int:
        try:
            return self._dict[sid]
        except KeyError:
            logger.warning(f"No such nid in remnode table for sid: {sid}")
