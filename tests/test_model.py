from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("BAAI/bge-large-en-v1.5")

print("Loaded successfully!")

embedding = model.encode("Hello World")

print(embedding.shape)