import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.kg.kg_service import KnowledgeGraphService

kg = KnowledgeGraphService()

entities = [

    "Embeddings",

    "Ranking",

    "Vector Databases"

]

expanded = kg.expand(entities)

print()

for item in expanded:

    print(item)