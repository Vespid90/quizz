import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    @staticmethod
    def get_connection():
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            host=os.getenv('DB_HOST'),
            password=os.getenv('DB_PWD'))
        return conn


db = Config.get_connection()
cur = db.cursor()