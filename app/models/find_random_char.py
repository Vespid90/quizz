import requests

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
            "manga": [entry["name"] for entry in data.get("manga", [])]
        }

        return character_info
    else:
        print(f"Erreur {response.status_code} lors de l’appel API")
        return None


perso = fetch_random_character()
if perso:
    print(f"Nom : {perso['nom']}")
    print(f"Image : {perso['image_url']}")
    print(f"Apparaît dans : {perso['anime']}")
