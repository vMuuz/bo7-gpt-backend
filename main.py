from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import json
import os

# ---- Data model ----

class Doc(BaseModel):
    id: str
    title: str
    date: Optional[str] = None
    section: Optional[str] = None
    content: str
    source: Optional[str] = None

# ---- App ----

app = FastAPI(title="BO7 Knowledge API")

DATA_PATH = "data/base_docs.json"
docs: List[Doc] = []


def load_docs():
    global docs
    if not os.path.exists(DATA_PATH):
        docs = []
        return
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    docs = [Doc(**item) for item in raw]


@app.on_event("startup")
def startup_event():
    load_docs()


@app.get("/")
def home():
    return {"status": "BO7 backend running", "num_docs": len(docs)}


@app.get("/search")
def search(
    query: str = Query(..., description="Search text"),
    limit: int = Query(5, ge=1, le=20)
):
    """
    Very simple search: returns docs whose title or content contains the query text.
    """
    if not docs:
        return {"results": []}

    q = query.lower()
    matches = [
        d for d in docs
        if q in d.title.lower() or q in d.content.lower()
    ]

    if not matches:
        matches = docs  # fallback: just return first docs

    results = [d.model_dump() for d_]()
