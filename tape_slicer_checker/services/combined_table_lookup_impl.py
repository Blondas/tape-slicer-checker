from typing import Dict, Tuple
import logging

from tape_slicer_checker.db2.db2_connection import DB2Connection
from tape_slicer_checker.services.combined_table_lookup import CombinedTableLookup

logger = logging.getLogger(__name__)

class CombinedTableLookupImpl(CombinedTableLookup):
    def __init__(
        self,
        db2_connection: DB2Connection,
        tape_name: str
    ) -> None:
        self._db2_connection = db2_connection
        self._tape_name = tape_name
        self._dict: Dict[str, Tuple[str, int]] = self._fetch()
        self._dict: Dict[str, Tuple[str, int]] = self._fetch()
        logger.info(f"Dictionary size: {len(self._dict)}")
        logger.debug(f"Dictionary elements: {self._dict}")

    def _fetch(self) -> Dict[str, Tuple[str, int]]:
        with self._db2_connection.connect() as connection:
            query: str = (f"SELECT ag.agid_name, trim(ag.name), n.nid FROM remag ag "
                          f"inner join remnode n "
                          f"on ag.sid = n.sid "
                          f"inner join remtapevol t "
                          f"on n.name like '%'||trim(t.storgrp)||'%' "
                          f"and trim(t.volser) = '{self._tape_name}'"
                          )
            cursor = connection.cursor()
            cursor.execute(query)
            return {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
        
    def agname_nid(self, agid_name: str) -> Tuple[str, int]:
        try:
            return self._dict[agid_name]
        except KeyError:
            logger.warning(f"No such agname: {agid_name}, nid in lookup query")