import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class ConnectPostgres:
    @staticmethod
    def get_connection():
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME_database'),
                user=os.getenv('DB_USER'),
                host=os.getenv('DB_HOST'),
                password=os.getenv('DB_PWD')
            )
            return conn
        except psycopg2.OperationalError as e:
            print(e)

class ConnectQuizzDb:
    @staticmethod
    def get_connection():
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                host=os.getenv('DB_HOST'),
                password=os.getenv('DB_PWD')
            )
            return conn
        except psycopg2.OperationalError as e:
            print(e)

class DisconnectQuizzDb:
    @staticmethod
    def disconnect_db(db):
        try:
            db.close()
        except Exception as e:
            print("erreur:", e)



#exemple de query solide
# db = ConnectQuizzDb.get_connection()
# cur = db.cursor()
#
# class Query1:
#     @staticmethod
#     def query_1(cur, db):
#         try:
#             cur.execute(""" INSERT INTO person (name) VALUES (Naruto) """)
#         except Exception as e:
#             print ("Erreur: ", e)
#         finally:
#             db.commit()
#             cur.close()
