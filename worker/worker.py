import random
import requests
import time

print("Worker started")

def get_random_word() -> str | None:
    try:
        with open("words_dictionary.txt", "r") as dict_file:
            words = dict_file.read().splitlines()
            return random.choice(words)
    except FileNotFoundError:
        return None

def main():
    word = get_random_word()

    if not word:
        return

    print(f"Selected word: {word}")
    
    time.sleep(2)
    try:
        response = requests.get(f"http://api:8000/random-word/{word}")
        if response.status_code == 200:
            print("Mot enregistre avec succes dans l'API !")
            return
    except Exception as e:
        raise Exception(f"Erreur lors de l'enregistrement du mot dans l'API : {e}")

main()

print("Worker exiting cleanly")