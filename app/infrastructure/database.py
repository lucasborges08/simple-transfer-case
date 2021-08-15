import logging
import sys

import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from app.config import settings

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)

DB_POOL = None


def get_pool():
    """
    Make the database connection inside method call to avoid database not exist
    during testing which will auto create/drop test database
    """
    global DB_POOL
    if DB_POOL is None:
        DB_POOL = pool.ThreadedConnectionPool(minconn=10,
                                              maxconn=15,
                                              user=settings.POSTGRES_USERNAME,
                                              password=settings.POSTGRES_PASSWORD,
                                              database=settings.POSTGRES_DATABASE,
                                              host=settings.POSTGRES_HOST)
    return DB_POOL


@contextmanager
def get_conn():  # noqa
    db_pool = get_pool()
    conn = db_pool.getconn()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        yield conn, cursor
        conn.commit()
    except psycopg2.Error as error:
        conn.rollback()
        LOG.error(error.pgerror)
        LOG.error(error.diag.message_detail)
        raise error
    except Exception as error:
        conn.rollback()
        raise error
    finally:
        cursor.close()
        db_pool.putconn(conn)
