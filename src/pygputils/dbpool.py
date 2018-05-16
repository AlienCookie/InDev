import os

import psycopg2

from eventlet.db_pool import ConnectionPool

from pygputils.db import DB
from pygputils import get_logger
logger = get_logger('dbpool')

POOL = ConnectionPool(psycopg2,
                      dbname=os.environ['GP_DATABASE_DB'],
                      user=os.environ['GP_DATABASE_USER'],
                      password=os.environ['GP_DATABASE_PASSWORD'],
                      host=os.environ['GP_DATABASE_HOST'],
                      port=os.environ['GP_DATABASE_PORT'],
                      min_size=0,
                      max_size=10)

def get():
    conn = POOL.get()
    return DB(conn)

def put(db):
    try:
        db.rollback()
    except Exception as e:
        logger.exception(e)

    POOL.put(db.conn)
    db.conn = None
