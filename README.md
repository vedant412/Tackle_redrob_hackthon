# REDROB AI - Intelligent Candidate Ranking System

An end-to-end AI-powered candidate retrieval and ranking system built for the **REDROB Hackathon**.

The system transforms an unstructured job description into a ranked list of the top 100 candidates using LLMs, hybrid retrieval, feature engineering, weighted ranking, and explainable AI.

---

## Pipeline Architecture

```
Job Description
        │
        ▼
LLM Job Parser
        │
        ▼
HYRE Profile Generator
        │
        ▼
Knowledge Graph Expansion
        │
        ▼
Positive & Negative Query Generation
        │
        ▼
Hybrid Retrieval
(Dense + BM25)
        │
        ▼
Reciprocal Rank Fusion (RRF)
        │
        ▼
Top Candidate Retrieval
        │
        ▼
Candidate Enrichment
        │
        ▼
Hard Constraint Filtering
        │
        ▼
Feature Engineering
(Honeypot detection from feature engineering)
        │
        ▼
Weighted Ranking 
        │
        ▼
Candidate Explanation Generation
        │
        ▼
CSV Submission Export
```

---

# Features

- LLM-based Job Parsing
- HYRE Profile Generation
- Knowledge Graph Query Expansion
- Positive & Negative Query Generation
- Dense Semantic Retrieval (FAISS + BGE)
- BM25 Lexical Retrieval
- Reciprocal Rank Fusion (RRF)
- Candidate Enrichment
- Hard Constraint Filtering
- Feature Engineering
- Weighted Ranking Model
- Explainable Candidate Ranking
- Submission CSV Generation

---

# Project Structure

```
backend/
│
├── app/
│   ├── api/
│   ├── builders/
│   ├── explanations/
│   ├── exporters/
│   ├── filtering/
│   ├── kg/
│   ├── llm/
│   ├── models/
│   ├── pipeline/
│   ├── prompts/
│   ├── ranking/
│   ├── retrieval/
│   ├── services/
│   └── utils/
│
├── data/
├── sample_data/
├── tests/
├── outputs/
├── requirements.txt
└── main.py
```

---

# Technology Stack

### AI / NLP

- Google Gemini
- Groq LLM
- Sentence Transformers (BGE Large)
- FAISS
- BM25

### Machine Learning

- Scikit-learn
- LightGBM (Architecture Ready)
- Feature Engineering

### Backend

- Python
- Pydantic
- Pandas
- NumPy

---

# Retrieval Pipeline

Hybrid retrieval combines:

- Dense Semantic Search
- BM25 Keyword Search
- Reciprocal Rank Fusion

to maximize recall before ranking.

---

# Ranking Features

The ranking model considers multiple signals including:

- Semantic Similarity
- BM25 Score
- RRF Score
- Skill Overlap
- Preferred Skill Match
- Experience Gap
- Current Title Similarity
- Industry Match
- Location Match
- Recruiter Response Rate
- GitHub Activity Score
- Profile Completeness

---

# Explainability

Each ranked candidate is accompanied by a human-readable explanation describing why they were ranked highly.

Example:

> Ranked highly due to strong semantic similarity with the job requirements, high skill overlap, relevant experience, and excellent recruiter engagement signals.

---

# Output

The pipeline generates:

```
outputs/final_submission.csv
```

Example columns:

| Column | Description |
|----------|------------|
| candidate_id | Candidate ID |
| rank | Final Rank |
| score | Ranking Score |
| reasoning | Explanation for Ranking |

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Tackle_redrob_hackthon.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run

Execute the complete pipeline:

```bash
python tests/test_pipeline.py
```

The ranked candidate list will be generated inside:

```
outputs/final_submission.csv
```

---

# Future Improvements

- Learning-to-Rank (LightGBM Ranker)
- Cross Encoder Re-ranking
- SHAP-based Feature Explainability
- Recruiter Feedback Learning
- Online Ranking Updates
- Multi-language Job Parsing
- Graph Neural Network Candidate Matching

---

# Team

Developed for the **REDROB AI Hiring Hackathon**.

---

# License

This project was developed for educational and hackathon purposes.
