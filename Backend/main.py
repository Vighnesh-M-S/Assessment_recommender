from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import uvicorn
import math

# Load environment variables and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# Load vector index and dataframe
index = faiss.read_index("shl_vector_index.faiss")
df = pd.read_csv("shl_combined_assessments.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")

# FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="Static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend origin like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # allows all HTTP methods including OPTIONS
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    return FileResponse(os.path.join("Static", "index.html"))

# Request schema
class Query(BaseModel):
    query: str

# Format result
def format_row(row):
    def safe_cast(val, cast_type, default):
        try:
            if val is None or (isinstance(val, float) and math.isnan(val)):
                return default
            return cast_type(val)
        except Exception:
            return default

    return {
        "Assignment_Name": str(row["Assignment_Name"]),
        "Assignment_Link": str(row["Assignment_Link"]),
        "Test_Type": str(row["Test_Type"]),
        "Approximate_Completion_Time": safe_cast(row["Approximate_Completion_Time"], int, -1),
        "Remote_Testing_Support": bool(row["Remote_Testing_Support"]),
        "Adaptive_IRT_Support": bool(row["Adaptive_IRT_Support"]),
        "Job_Levels": str(row.get("Job_Levels", "N/A")),
    }

# API endpoint
@app.post("/query")
async def query_assessments(payload: Query):
    query_embedding = model.encode([payload.query]).astype("float32")
    D, I = index.search(query_embedding, 10)  # Top 10 results

    results = [format_row(df.iloc[idx]) for idx in I[0]]
    return {"query": payload.query, "recommendations": results}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)