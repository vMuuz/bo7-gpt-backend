from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "BO7 backend running"}
