import requests

class FetchAnime:
    @staticmethod
    def fetch_random_anime():
        url = "https://api.jikan.moe/v4/random/anime"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()["data"]

            anime_info = {
                "mal_id": data.get("mal_id"),
                "url": data.get("url"),
                "image1": data.get("images", {}).get("jpg", {}).get("image_url"),
                "image2": data.get("images", {}).get("jpg", {}).get("small_image_url"),
                "image3": data.get("images", {}).get("jpg", {}).get("large_image_url"),
                "title": data.get("title"),
                "year": data.get("year")
            }
            return anime_info

        else:
            print(f"Erreur {response.status_code} lors de l’appel API")
            return None

anime = FetchAnime.fetch_random_anime()
if anime:
    print(f"Nom : {anime['title']}")
    print(f"Image: {anime['image1']}")
    print(f"Année : {anime['year']}")