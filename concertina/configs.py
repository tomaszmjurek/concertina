import os
import psycopg2

USER = 'aleksykrolczyk'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'concertina_test'

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                    'postgresql://localhost/concertina'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def connect_db():
    try:
        connection = psycopg2.connect(
            user=USER,
            host=HOST,
            port=PORT,
            database=DB_NAME
        )
        connection.autocommit = True
        return connection
    except:
        print("Could not connect to the DB")