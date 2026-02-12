import random
import requests
import time
import unicodedata

print("Worker started")

def remove_accents(word: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', word)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
def get_random_word_from_api() -> str | None:
    try:
        response = requests.get("https://trouve-mot.fr/api/random", timeout=5)
        raw_word = response.json()[0]['name']
        word = remove_accents(raw_word)
        return word.upper()
    except requests.RequestException as e:
        print(f"⚠️ Erreur API publique : {e}")
        return None

def get_random_word_from_dictionary() -> str | None:
    try:
        with open("words_dictionary.txt", "r") as dict_file:
            words = dict_file.read().splitlines()
            return random.choice(words)
    except FileNotFoundError:
        print("⚠️ Dictionnaire local introuvable")
        return None

def main():
    word = get_random_word_from_api()
    
    if not word:
        print("Echec de l'appel à l'API publique, utilisation du dictionnaire local")
        word = get_random_word_from_dictionary()
        if not word:
            raise Exception("❌ Erreur: Aucun mot trouvé.")

    print(f"Mot sélectionné: {word}")
    
    time.sleep(1)
    try:
        response = requests.get(f"http://api:8000/random-word/{word}")
        if response.status_code == 200:
            print("✅ Mot enregistre avec succes dans l'API !")
            return
    except Exception as e:
        raise Exception(f"❌ Erreur lors de l'enregistrement du mot dans l'API : {e}")

main()

print("Worker exiting cleanly")