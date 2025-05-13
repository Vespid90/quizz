from app.config import ConnectQuizzDb

class AddChar:
    @staticmethod
    def add_char(char, images):
        db = ConnectQuizzDb.get_connection()
        cur = db.cursor()
        try:
            anime_list = char.get("anime", [])
            anime_name = anime_list[0] if isinstance(anime_list, list) and len(anime_list) > 0 else "Pas de nom d'anime"

            cur.execute("""
            INSERT INTO person (name, image1, image2, image3, anime_name) 
            VALUES (%s, %s, %s, %s, %s)
            """, (
                char["nom"],
                images[0],
                images[1],
                images[2],
                anime_name,
            ))
            db.commit()
            print("info mise en db")
        except Exception as e:
            print("Erreur:", e)
        finally:
            cur.close()
            db.close()