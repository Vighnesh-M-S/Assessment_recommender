from fastapi import FastAPI, Request
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend origin like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # allows all HTTP methods including OPTIONS
    allow_headers=["*"],
)

class QueryInput(BaseModel):
    text: str

@app.post("/query_assessments/")
async def query_assessments(data: QueryInput):
    user_input = data.text

    # Prompt Gemini for NLP extraction
    gemini_prompt = f"""
    Extract the following from the query:
    1. Programming languages
    2. Roles (e.g., developer, analyst, director)
    3. Level (e.g., entry-level, mid-level, senior)
    4. Assessment types (like cognitive, technical, personality, communication)
    5. Time limit in minutes

    Respond only in dictionary like this:
    {{
  "languages": ["Python", "SQL", "JavaScript"],
  "roles": ["professionals"],
  "level": ["mid-level"],
  "assessment_types": ["skills"],
  "time_limit_minutes": 60
}}

    Query:
    \"\"\"{user_input}\"\"\"
    """
    gemini_response = gemini_model.generate_content(gemini_prompt)
    # print("Gemini response status:", gemini_response.status_code)
    # print("Gemini response text:", gemini_response.text)
    structured = json.loads(gemini_response.text[8:-3])
    print(structured)

    # Build a new semantic query string from extracted data
    query_components = structured["languages"] + structured["roles"] + structured["level"] + structured["assessment_types"]
    query_components.append(f"{structured['time_limit_minutes']} minutes")
    final_query = " ".join(query_components)

    # Search vector DB
    embedding = model.encode([final_query]).astype("float32")
    D, I = index.search(embedding, 10)

    # Fallback if nothing found (all scores 0.0 or similar)
    top_matches = []
    for idx in I[0]:
        if idx < len(df):
            row = df.iloc[idx]
            top_matches.append({
                "name": row["Assignment_Name"],
                "url": row["Assignment_Link"],
                "type": row["Test_Type"],
                "duration": row["Approximate_Completion_Time"],
                "adaptive": row["Adaptive_IRT_Support"],
                "remote": row["Remote_Testing_Support"]
            })

    if not top_matches:
        top_matches = [{
            "name": df.iloc[0]["Assignment_Name"],
            "url": df.iloc[0]["Assignment_Link"],
            "type": df.iloc[0]["Test_Type"],
            "duration": df.iloc[0]["Approximate_Completion_Time"],
            "adaptive": df.iloc[0]["Adaptive_IRT_Support"],
            "remote": df.iloc[0]["Remote_Testing_Support"]
        }]

    return {
        "query_extracted": structured,
        "top_matches": top_matches
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)