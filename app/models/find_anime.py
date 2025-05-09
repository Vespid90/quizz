import requests

def find_anime(titre, limit=3):
    url = "https://api.jikan.moe/v4/anime/{id}/characters"
    params = {
        "q": titre,
        "limit": limit,
        "order_by": "title",
        "sort": "asc",
        "sfw": True
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        resul = response.json()["data"]
        for index, anime in enumerate(resul, 1):
            print(f"\n Résultat {index}")
            print("Titre:", anime['title'])
    else:
        print(f"Erreur ({response.status_code}): {response.json().get('error')}")


find_anime("20")
