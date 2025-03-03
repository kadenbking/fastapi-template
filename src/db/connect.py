from fastapi import HTTPException
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool
from typing import Any, Dict, List, Tuple

from config import Settings

settings = Settings()

DB_CONFIG = {
    "host": settings.DB_HOST,
    "user": settings.DB_USER,
    "port": settings.DB_PORT,
    "password": settings.DB_PASSWORD,
    "database": settings.DB_NAME,
    "connection_timeout": 5,
}

pool = MySQLConnectionPool(pool_name="pool", pool_size=10, **DB_CONFIG)


def fetch_rows(query: str, params: Tuple) -> List[Dict[str, Any]]:
    connection = pool.get_connection()

    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()


def insert_row(query: str, params: Tuple):
    connection = pool.get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()
