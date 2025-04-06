# 🧠 SHL Assessment Recommendation System

This is a GenAI-powered application that recommends the most relevant SHL assessments based on a user's natural language query or job description. It includes a FastAPI backend, a static HTML/JS/CSS frontend, and an in-memory vector search using sentence embeddings.

Live Link : [https://assessment-recommender-new.onrender.com](https://assessment-recommender-new.onrender.com))

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
├── Backend/
│   ├── main.py               # FastAPI backend
│   ├── requirements.txt      # Python dependencies
├── Frontend/
│   ├── index.html            # Frontend UI
│   ├── styles.css            # Styling
│   └── script.js             # Frontend logic (querying backend)
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
pip install -r Backend/requirements.txt
```

### 4. Run the Backend Server

```bash
uvicorn Backend.main:app --reload
```

By default, the backend runs at: `http://127.0.0.1:8000`

---

## 🌐 Frontend Usage

Open the `Frontend/index.html` file in a browser.

The frontend sends queries to the FastAPI backend and displays the top SHL assessments relevant to the user's input.

---

## 🧪 Example Query

Try inputting:

> "We're hiring a senior software engineer with strong coding and problem-solving skills."

The system will return the top 10 SHL assessments based on semantic similarity.

---

## 🛠 Tech Stack

- 🐍 Python 3.10+
- 🦋 FastAPI
- 🤗 Sentence Transformers (`all-MiniLM-L6-v2`)
- 🧠 FAISS for vector search
- 🔧 HTML/CSS/JavaScript
- 🖼️ Pandas for tabular data processing

---

## 🚢 Deployment (Render)

1. Go to [https://assessment-recommender-new.onrender.com](https://assessment-recommender-new.onrender.com))

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
