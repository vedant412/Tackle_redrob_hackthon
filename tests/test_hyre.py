import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv

from app.llm import LLMRouter
from app.services.llm_job_parser import LLMJobParser
from app.services.hyre_generator import HYREGenerator

load_dotenv()


provider = LLMRouter()

parser = LLMJobParser(provider)

hyre = HYREGenerator(provider)

job_path = (
    BASE_DIR
    / "sample_data"
    / "job_descriptions"
    / "redrob_ai_engineer.txt"
)

jd = job_path.read_text(encoding="utf8")

parsed = parser.parse(jd)

profile = hyre.generate(parsed)

print(profile.model_dump_json(indent=4))