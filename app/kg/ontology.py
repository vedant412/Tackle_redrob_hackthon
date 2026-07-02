KG = {

    "Embeddings": {

        "aliases": [
            "Embedding Models",
            "Vector Embeddings"
        ],

        "children": [
            "Sentence Transformers",
            "BGE",
            "E5",
            "OpenAI Embeddings",
            "Voyage",
            "Jina Embeddings"
        ],

        "related": [
            "Retrieval",
            "Semantic Search",
            "Vector Database"
        ]
    },

    "Retrieval": {

        "aliases": [
            "Search",
            "Semantic Search"
        ],

        "children": [
            "Dense Retrieval",
            "Hybrid Retrieval",
            "Sparse Retrieval",
            "BM25"
        ],

        "related": [
            "Embeddings",
            "Ranking"
        ]
    },

    "Ranking": {

        "aliases": [
            "Learning To Rank"
        ],

        "children": [
            "LambdaMART",
            "LightGBM Ranker",
            "XGBoost Ranker",
            "Cross Encoder",
            "ColBERT",
            "SPLADE"
        ],

        "related": [
            "Retrieval",
            "NDCG",
            "MRR"
        ]
    },

    "Vector Databases": {

        "aliases": [
            "Vector Store"
        ],

        "children": [
            "FAISS",
            "Milvus",
            "Qdrant",
            "Pinecone",
            "Weaviate",
            "Chroma"
        ],

        "related": [
            "Embeddings"
        ]
    }

}