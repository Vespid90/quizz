from app.config import ConnectQuizzDb as Quizz, ConnectPostgres
from psycopg2 import errors


class DropDb:
    @staticmethod
    def drop_db():
        db = ConnectPostgres.get_connection()
        db.autocommit = True
        cur = db.cursor()
        try:
            cur.execute(""" DROP DATABASE quizz_db""")
            print("quizz_db bien supprimée")
        except Exception as e:
            print("Erreur:", e)
        finally:
            cur.close()
            db.close()

class CreateDb:
    @staticmethod
    def create_db():
        db = ConnectPostgres.get_connection()
        db.autocommit = True
        cur = db.cursor()
        try:
            cur.execute(""" CREATE DATABASE quizz_db""")
            print("quizz_db a été créée")
        except errors.DuplicateDatabase:
            print("quizz_db existe déjà")
        except Exception as e:
            print("Erreur:", e)
        finally:
            cur.close()
            db.close()

class CreateTable:
    @staticmethod
    def create_table():
        db = Quizz.get_connection()
        cur = db.cursor()
        try:
            cur.execute(""" CREATE TABLE IF NOT EXISTS users (
                                    id_users SERIAL PRIMARY KEY,
                                    first_name VARCHAR(100) NOT NULL,
                                    last_name VARCHAR(100) NOT NULL,
                                    password VARCHAR(255) NOT NULL,
                                    email VARCHAR(255) UNIQUE NOT NULL,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                                    """)

            cur.execute(""" CREATE TABLE IF NOT EXISTS person (
                                    id_person SERIAL PRIMARY KEY,
                                    name VARCHAR(255),
                                    image_url TEXT,
                                    image2_url TEXT,
                                    image3_url TEXT,
                                    anime_id INTEGER,
                                    anime_name VARCHAR(255),
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """)

            cur.execute(""" CREATE TABLE IF NOT EXISTS ranking (
                                    id_ranking SERIAL PRIMARY KEY,
                                    id_users INTEGER NOT NULL,
                                    score INT NOT NULL,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    FOREIGN KEY (id_users) REFERENCES users(id_users))
                                    """)
            print("Tables créées")
        except Exception as e:
            print("Erreur:", e)
        finally:
            db.commit()
            cur.close()
            db.close()

DropDb.drop_db()
CreateDb.create_db()
CreateTable.create_table()