import random
import time

def get_random_word():
    with open("words_dictionary.txt", "r") as dict_file:
        words = dict_file.read().splitlines()
    return random.choice(words)

print("Worker started")
print(get_random_word())
print("Worker exiting cleanly")