import os, requests
from urllib.parse import urlparse
from app.config import ConnectQuizzDb



class AddChar:
    @staticmethod
    def download_and_rename_image(image_url, name):
        safe_name = name.replace(" ", "_").replace("/", "_") + ".jpg"
        image_path = os.path.join("../", "static", "img", safe_name)

        if not os.path.exists(image_path):
            print(f"image téléchargée {name}...")
            try:
                img_data = requests.get(image_url).content
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, 'wb') as f:
                    f.write(img_data)
            except Exception as e:
                print(f"Erreur: {e}")
                return None
        return safe_name

    @staticmethod
    def add_char(char):
        db = ConnectQuizzDb.get_connection()
        cur = db.cursor()
        try:
            anime_list = char.get("anime", [])
            anime_name = anime_list[0] if isinstance(anime_list, list) and len(anime_list) > 0 else "Pas de nom d'anime"

            image_filename = AddChar.download_and_rename_image(char["image_url"], char["nom"])

            cur.execute("SELECT id_person FROM person WHERE mal_id = %s", (char["mal_id"],))
            if cur.fetchone():
                print("Personnage déjà présente dans la db")
                return
            else:
                cur.execute("""
                INSERT INTO person (mal_id, name, image1, image2, image3, anime_name) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    char["mal_id"],
                    char["nom"],
                    image_filename,
                    image_filename,
                    image_filename,
                    anime_name,
                    ))
                db.commit()
                print("info mise en db")
        except Exception as e:
            print("Erreur:", e)
        finally:
            cur.close()
            db.close()