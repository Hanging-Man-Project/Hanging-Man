from fastapi import FastAPI, HTTPException
import httpx
import uuid

app = FastAPI()

WORKER_URL = "http://worker:8000/random-word"

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/start")
async def start_game(request: StartRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(WORKER_URL)
            response.raise_for_status()
            data = response.json()
            word = data.get("word", "")

            masked_word = "_" * len(word)
            
            return {
                "game_id": str(uuid.uuid4())[:6], 
                "letters": masked_word
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur Worker: {str(e)}")