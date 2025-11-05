from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI(title="Roulette API")

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load options
DATA_DIR = "app/data"

with open(f"{DATA_DIR}/options.json", "r", encoding="utf-8") as f:
    OPTIONS = json.load(f)

with open(f"{DATA_DIR}/questions.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)


@app.get("/options")
def get_options():
    """Return all roulette options."""
    return {"options": OPTIONS}


@app.get("/result/{option_id}")
def get_result(option_id: int):
    """Return the result for a selected option."""
    option = next((opt for opt in OPTIONS if opt["id"] == option_id), None)
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")

    if option["type"] == "prize":
        return {"message": option['label']}
    elif option["type"] == "python_question":
        return {"question": random.choice(QUESTIONS["python"])}
    elif option["type"] == "make_question":
        return {"question": random.choice(QUESTIONS["make"])}
    else:
        return {"message": "Try again!"}
