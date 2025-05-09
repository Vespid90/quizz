from app.config import DisconnectQuizzDb, ConnectQuizzDb

db = ConnectQuizzDb.get_connection()

DisconnectQuizzDb().disconnect_db(db)