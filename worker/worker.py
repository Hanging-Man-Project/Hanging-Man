import random
import requests
import unicodedata
from flask import Flask, jsonify

app = Flask(__name__)

print("🚀 Worker started.")

   
def get_random_word_from_api() -> str | None:
    """Retrieves a random word from a public API."""
    try:
        response = requests.get(f"https://random-word-api.herokuapp.com/word?length={random.randint(5, 9)}&diff={random.randint(1, 2)}", timeout=5)
        word = response.json()[0]
        return word.upper()
    except requests.RequestException as e:
        print(f"⚠️ Public API error: {e}")
        return None

def get_random_word_from_dictionary() -> str | None:
    """Retrieves a random word from a local dictionary."""
    try:
        with open("words_dictionary.txt", "r") as dict_file:
            words = dict_file.read().splitlines()
            return random.choice(words).upper()
    except FileNotFoundError:
        print("⚠️ Local dictionary not found.")
        return None

@app.route("/random-word", methods=["GET"])
def random_word():
    """Generate a random word."""
    word = get_random_word_from_api()
    
    if not word:
        word = get_random_word_from_dictionary()
        if not word:
            return jsonify({"error": "❌ No words found"}), 500

    print(f"✅ Generated word: {word}")
    return jsonify({"word": word}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)