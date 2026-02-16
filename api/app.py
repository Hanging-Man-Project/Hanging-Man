from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
import httpx
import uuid

app = FastAPI()

# Structure for storing current parts (in memory)
games: Dict[str, dict] = {}

class StartGameRequest(BaseModel):
    max_attempts: int = Field(default=6, description="Nombre maximum de tentatives")

class GuessRequest(BaseModel):
    game_id: str = Field(..., description="ID de la partie")
    letter: str = Field(..., min_length=1, max_length=1, description="Lettre à deviner")

class GameStatus(BaseModel):
    game_id: str
    letters: str
    guessed_letters: list
    attempts_left: int
    status: str  # "in_progress", "won", "lost"

word : str = ""


@app.get("/")
def root():
    return {"message": "🚀 Hanging Man API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/start", response_model=GameStatus)
async def start_game(request: StartGameRequest = StartGameRequest()):
    """Start a new game with a random word from the worker."""
    
    # Retrieving a random word from the worker
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://worker:5001/random-word", timeout=5.0)
            response.raise_for_status()
            word = response.json().get("word", "").upper()
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail=f"❌ Unable to retrieve a word from the worker: {str(e)}"
        )
    
    if not word:
        raise HTTPException(status_code=500, detail="❌ No word received from the worker")
    
    # Creating a new game
    game_id = str(uuid.uuid4())
    games[game_id] = {
        "word": word,
        "guessed_letters": set(),
        "attempts_left": request.max_attempts,
        "status": "in_progress"
    }
    
    # Construction of the initial hidden word
    masked_word = " ".join(["_" if c.isalpha() else c for c in word])
    
    return GameStatus(
        game_id=game_id,
        letters=masked_word,
        guessed_letters=[],
        attempts_left=request.max_attempts,
        status="in_progress"
    )


@app.post("/guess", response_model=GameStatus)
async def guess_letter(guess: GuessRequest):
    game_id = guess.game_id
    letter = guess.letter.upper()

    # Verification of the existence of the party
    if game_id not in games:
        raise HTTPException(status_code=404, detail="❌ Party not found")

    game = games[game_id]

    # Verifying the status of the party
    if game["status"] != "in_progress":
        raise HTTPException(
            status_code=400, 
            detail=f"The game is over: {game['status']}"
        )

    # Letter validation
    if not letter.isalpha():
        raise HTTPException(status_code=400, detail="⚠️ Only letters are allowed.")

    # Checking whether the letter has already been guessed
    if letter in game["guessed_letters"]:
        raise HTTPException(status_code=400, detail="⚠️ Letter already guessed")

    # Adding the letter to the guessed letters
    game["guessed_letters"].add(letter)

    # Checking if the letter is in the word
    if letter not in game["word"]:
        game["attempts_left"] -= 1

    # Construction of the hidden word
    masked_word = " ".join([
        c if c in game["guessed_letters"] or not c.isalpha() else "_"
        for c in game["word"]
    ])

    # Checking victory/defeat conditions
    if "_" not in masked_word:
        game["status"] = "won"
    # Reveal the word if the game is lost
    elif game["attempts_left"] <= 0:
        game["status"] = "lost"
        masked_word = " ".join(game["word"])

    return GameStatus(
        game_id=game_id,
        letters=masked_word,
        guessed_letters=sorted(list(game["guessed_letters"])),
        attempts_left=game["attempts_left"],
        status=game["status"]
    )


@app.get("/status/{game_id}", response_model=GameStatus)
async def get_game_status(game_id: str):
    """Retrieves the status of a game."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="❌ Party not found.")

    game = games[game_id]

    # Construction of the hidden word
    if game["status"] == "lost":
        masked_word = " ".join(game["word"])
    else:
        masked_word = " ".join([
            c if c in game["guessed_letters"] or not c.isalpha() else "_"
            for c in game["word"]
        ])

    return GameStatus(
        game_id=game_id,
        letters=masked_word,
        guessed_letters=sorted(list(game["guessed_letters"])),
        attempts_left=game["attempts_left"],
        status=game["status"]
    )


@app.delete("/game/{game_id}")
async def delete_game(game_id: str):
    """Deletes a porty."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="❌ Party not found")
    
    del games[game_id]
    return {"message": "Deleted section", "game_id": game_id}

@app.get("/games")
async def list_games():
    """List all ongoing parties."""
    return {
        "total_games": len(games),
        "games": [
            {
                "game_id": gid,
                "status": game["status"],
                "attempts_left": game["attempts_left"]
            }
            for gid, game in games.items()
        ]
    }


@app.get("/random-word/{random_word}")
def set_word(random_word: str):
    global word

    if not random_word:
        raise HTTPException(status_code=400, detail="❌ Required word parameter is missing")
    
    word = random_word
    
    return word
