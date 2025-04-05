from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load model, index and metadata
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("shl_faiss.index")
metadata = pd.read_csv("shl_metadata.csv")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict it later
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/recommend")
def recommend_tests(req: QueryRequest):
    query_embed = model.encode([req.query])
    distances, indices = index.search(query_embed, req.top_k)

    results = []
    for idx in indices[0]:
        item = metadata.iloc[idx]
        results.append({
            "assessment_name": item["assessment_name"],
            "assessment_url": item["assessment_url"],
            "remote_support": item["remote_support"],
            "adaptive_support": item["adaptive_support"],
            "duration": item["duration"],
            "test_type": item["test_type"]
        })

    return {"query": req.query, "recommendations": results}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)