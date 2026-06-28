import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    with open("./models/face_detection.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data