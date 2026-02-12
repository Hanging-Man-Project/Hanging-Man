from fastapi import FastAPI, HTTPException
import httpx
import uuid

app = FastAPI()

word : str = ""

@app.get("/")
def root():
    return {"message": word}

@app.get("/health")
def health():
    return {"status": "ok"}
        
@app.get("/random-word/{random_word}")
def set_word(random_word: str):
    global word

    if not random_word:
        print("No word provided")
        raise HTTPException(status_code=400, detail="Mot requis")
    
    word = random_word
    
    return word