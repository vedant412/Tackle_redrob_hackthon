from sentence_transformers import SentenceTransformer
import numpy as np
import torch


class EmbeddingService:

    def __init__(
        self,
        model_name="BAAI/bge-large-en-v1.5",
    ):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading {model_name} on {self.device}...")

        self.model = SentenceTransformer(
            model_name,
            device=self.device,
        )

        print("Embedding model loaded.")

    def encode(self, text: str):

        return self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

    def encode_batch(self, texts, batch_size=64):

        return self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True,
        )