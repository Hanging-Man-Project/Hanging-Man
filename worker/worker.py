import random
import requests
import unicodedata
from flask import Flask, jsonify

app = Flask(__name__)

print("🚀 Worker started as API service")

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
            return random.choice(words).upper()
    except FileNotFoundError:
        print("⚠️ Dictionnaire local introuvable")
        return None

@app.route("/random-word", methods=["GET"])
def random_word():
    """Génère un mot aléatoire"""
    word = get_random_word_from_api()
    
    if not word:
        print("Echec de l'appel à l'API publique, utilisation du dictionnaire local")
        word = get_random_word_from_dictionary()
        if not word:
            return jsonify({"error": "Aucun mot trouvé"}), 500

    print(f"✅ Mot généré: {word}")
    return jsonify({"word": word}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)