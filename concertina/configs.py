import os
import psycopg2
from psycopg2.extras import RealDictCursor

USER = 'postgres'
HOST = 'localhost'
PORT = '5433'
DB_NAME = 'concertina'


def connect_db():
    try:
        connection = psycopg2.connect(
            user=USER,
            host=HOST,
            password="dumbo",
            port=PORT,
            database=DB_NAME,
            cursor_factory=RealDictCursor,
        )
        connection.autocommit = True
        return connection
    except Exception as e:
        print(str(e))
