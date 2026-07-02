import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv

from app.llm import LLMRouter
from app.services.llm_job_parser import LLMJobParser
from app.services.hyre_generator import HYREGenerator
from app.retrieval.query_generator import QueryGenerator

load_dotenv()

provider = LLMRouter()

parser = LLMJobParser(provider)

hyre_generator = HYREGenerator(provider)

query_generator = QueryGenerator()

job_path = (
    BASE_DIR
    / "sample_data"
    / "job_descriptions"
    / "redrob_ai_engineer.txt"
)

jd = job_path.read_text(encoding="utf8")

parsed = parser.parse(jd)

hyre = hyre_generator.generate(parsed)

positive = query_generator.generate_positive(hyre)

negative = query_generator.generate_negative(hyre)

print("\n================ POSITIVE ================\n")

for q in positive:

    print(
    f"{q.weight:>5.2f} | "
    f"{q.category:<18} | "
    f"{q.text:<40} | "
    f"{', '.join(q.sources)}")

print("\n================ NEGATIVE ================\n")

for q in negative:

    print(
    f"{q.weight:>5.2f} | "
    f"{q.category:<18} | "
    f"{q.text:<40} | "
    f"{', '.join(q.sources)}")