import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# =====================================================
# Base Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROMPTS_DIR = BASE_DIR / "app" / "prompts"

# =====================================================
# API Keys
# =====================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =====================================================
# Models
# =====================================================

GEMINI_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"

# =====================================================
# Cache Directories
# =====================================================

CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# Embeddings

EMBEDDINGS_DIR = CACHE_DIR / "embeddings"
EMBEDDINGS_DIR.mkdir(exist_ok=True)

# BM25

BM25_DIR = CACHE_DIR / "bm25"
BM25_DIR.mkdir(exist_ok=True)

# LLM Cache

LLM_CACHE_DIR = CACHE_DIR / "llm"
LLM_CACHE_DIR.mkdir(exist_ok=True)

PARSED_JOB_CACHE = LLM_CACHE_DIR / "parsed_jobs"
PARSED_JOB_CACHE.mkdir(exist_ok=True)

HYRE_CACHE = LLM_CACHE_DIR / "hyre"
HYRE_CACHE.mkdir(exist_ok=True)

# =====================================================
# Cache Files
# =====================================================

EMBEDDINGS_PATH = EMBEDDINGS_DIR / "candidate_embeddings.npy"

CANDIDATE_IDS_PATH = EMBEDDINGS_DIR / "candidate_ids.npy"

CANDIDATE_DOCUMENTS_PATH = EMBEDDINGS_DIR / "candidate_documents.pkl"

FAISS_INDEX_PATH = EMBEDDINGS_DIR / "candidate.index"

BM25_INDEX_PATH = BM25_DIR / "bm25.pkl"

# =====================================
# Ranking
# =====================================

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

LIGHTGBM_MODEL_PATH = MODEL_DIR / "lightgbm_ranker.pkl"