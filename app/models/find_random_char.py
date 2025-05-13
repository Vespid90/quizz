from app.models.fetch_char import FetchChar
from app.models.add_char import AddChar

#https://docs.api.jikan.moe/#tag/random/operation/getRandomCharacters

class FindImage:
    @staticmethod
    def prepare_images(image_url):
        if image_url:
            return [image_url] * 3
        else:
            return [None, None, None]


char = FetchChar.fetch_random_character()
images = FindImage.prepare_images(char["image_url"])


perso = FetchChar.fetch_random_character()
AddChar.add_char(perso)
if perso:
    print(f"Nom : {perso['nom']}")
    print(f"Image : {perso['image_url']}")
    print(f"Apparaît dans : {perso['anime']}")
