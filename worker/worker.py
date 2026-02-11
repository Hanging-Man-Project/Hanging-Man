import random
import time

def get_random_word():
    try:
        with open("words_dictionary.txt", "r") as dict_file:
            words = dict_file.read().splitlines()
            return random.choice(words)
    except FileNotFoundError:
        return "ERREUR: Fichier introuvable"

print("Worker started")

word = get_random_word()
print(word)

print("Worker exiting cleanly")