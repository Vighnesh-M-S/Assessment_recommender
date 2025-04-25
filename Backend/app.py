import streamlit as st
import os
import pandas as pd
import faiss
import math
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# Load vector index and dataframe
index = faiss.read_index("shl_vector_index.faiss")
df = pd.read_csv("shl_combined_assessments.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Helper to format the result row
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

# Streamlit UI
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("🔍 SHL Assessment Recommender")

query = st.text_input("Enter your job role or requirement:", "")

if st.button("Search") and query:
    with st.spinner("Finding best assessments..."):
        query_embedding = model.encode([query]).astype("float32")
        D, I = index.search(query_embedding, 10)
        results = [format_row(df.iloc[idx]) for idx in I[0]]

    st.subheader("🔝 Top Recommendations")
    if results:
        for idx, r in enumerate(results, 1):
            with st.container():
                st.markdown(f"### 🏆 Rank {idx}: {r['Assignment_Name']}")
                st.markdown(f"[🔗 Assignment Link]({r['Assignment_Link']})")
                st.markdown(f"- 🧪 **Test Type**: {r['Test_Type']}")
                st.markdown(f"- ⏱️ **Duration**: {r['Approximate_Completion_Time']} mins")
                st.markdown(f"- 🌐 **Remote Testing**: {r['Remote_Testing_Support']}")
                st.markdown(f"- 📊 **Adaptive/IRT**: {r['Adaptive_IRT_Support']}")
                st.markdown(f"- 👤 **Job Levels**: {r['Job_Levels']}")
                st.markdown("---")
    else:
        st.warning("No results found.")
