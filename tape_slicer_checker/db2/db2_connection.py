from contextlib import contextmanager
from typing import Generator, Optional

from ibm_db_dbi import connect, Connection, Error as DB2Error
import logging

from tape_slicer_checker.config.tape_slicer_checker_config import DbConfig

logger = logging.getLogger(__name__)

class DB2Connection:
    def __init__(
        self,
        db_config: DbConfig
    ):
        self._database = db_config.database
        self._user = db_config.user
        self._password = db_config.password

    @contextmanager
    def connect(self) -> Generator[Connection, None, None]:
        conn: Optional[Connection] = None
        try:
            conn = connect(self._database, self._user, self._password)
            yield conn
        except DB2Error as e:
            logger.error("DB2 connection error",
                         extra={
                             'database': self._database,
                             'user': self._user,
                             'error_type': type(e).__name__
                         },
                         exc_info=e)
            raise
        except Exception as e:
            logger.error("Unexpected error during database connection",
                         extra={
                             'database': self._database,
                             'user': self._user,
                             'error_type': type(e).__name__
                         },
                         exc_info=e)
            raise
        finally:
            if conn is not None:
                conn.close()
