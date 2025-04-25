# 🧠 SHL Assessment Recommendation System

This is a GenAI-powered application that recommends the most relevant SHL assessments based on a user's natural language query or job description. It includes a FastAPI backend, a static HTML/JS/CSS frontend, and an in-memory vector search using sentence embeddings.

Live Link 1 : [https://assessment-recommender-new.onrender.com](https://assessment-recommender-new.onrender.com)
Live Link 2 : [https://assessment-recommender-new.onrender.com](https://assessment-recommender-new.onrender.com)

---

## 🚀 Features

- 🔍 Natural Language Query Input
- 📌 Top 10 Relevant SHL Assessments
- 🧠 Semantic Search using Sentence Transformers
- ⚡ FastAPI-powered REST API
- 🌐 Simple Frontend (HTML/CSS/JS)
- 🧾 SHL Assessment Catalog Integration
- ✅ Remote Testing / Adaptive IRT Support Indicators

---

## 📁 Project Structure

```
assignment recommender/
|
│── app.py               # FastAPI backend
│── requirements.txt      # Python dependencies
|── shl_combined_assessments.csv  
│── shl_vector_index.faiss     
│── render.yaml    
├── .env                      # Environment variables (if any)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/assignment-recommender.git
cd assignment-recommender
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Backend Server

```bash
uvicorn streamlit run app.py
```

---

## 🧪 Example Query

Try inputting:

> "We're hiring a senior software engineer with strong coding and problem-solving skills."

The system will return the top 10 SHL assessments based on semantic similarity.

---

## 🛠 Tech Stack

- 🐍 Python 3.10+
- 🎏 Streamlit
- 🤗 Sentence Transformers (`all-MiniLM-L6-v2`)
- 🧠 FAISS for vector search
- 🖼️ Pandas for tabular data processing

---

## 🚢 Deployment (Render)

1. Go to [https://assessment-recommender-new.onrender.com](https://huggingface.co/spaces/VGreatVig07/Assignment_Recommender)
2. Go to [https://assessment-recommender-new.onrender.com](https://assessment-recommender-new.onrender.com)

---

## 🤖 Future Improvements

- Integrate with real SHL catalog via Firecrawl + RAG pipeline
- Rerank results using LLM (e.g., GPT-4)
- Provide PDF/CSV export of recommendations
- Deploy as fullstack Docker container

---

## 📄 License

MIT License © 2025

---

## ✨ Acknowledgements

- [SHL](https://www.shl.com/)
- [SentenceTransformers](https://www.sbert.net/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
