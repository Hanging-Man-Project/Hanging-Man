import random
from fastapi import FastAPI, HTTPException

print("Worker started")

app = FastAPI()

def get_random_word() -> str | None:
    try:
        with open("words_dictionary.txt", "r") as dict_file:
            words = dict_file.read().splitlines()
            return random.choice(words)
    except FileNotFoundError:
        return None

@app.get("/random-word")
def random_word():
    word = get_random_word()

    if not word:
        raise HTTPException(status_code=404, detail="Aucun mot trouvé")

    return {"word": word}


print("Worker exiting cleanly")