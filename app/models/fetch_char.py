import requests

class FetchChar:
    @staticmethod
    def fetch_random_character():
        url = "https://api.jikan.moe/v4/random/characters"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()["data"]

            character_info = {
                "mal_id": data.get("mal_id"),
                "nom": data.get("name"),
                "nom_kanji": data.get("name_kanji"),
                "image_url": data.get("images", {}).get("jpg", {}).get("image_url"),
                "url": data.get("url"),
                "favoris": data.get("favorites"),
                "anime": [entry["name"] for entry in data.get("anime", [])],
            }

            return character_info
        else:
            print(f"Erreur {response.status_code} lors de l’appel API")
            return None