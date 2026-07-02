import sys
from pathlib import Path

# Add backend directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv

from app.llm import LLMRouter
from app.services.llm_job_parser import LLMJobParser

load_dotenv()


def main():

    provider = LLMRouter()

    parser = LLMJobParser(provider)

    job_path = (
        BASE_DIR
        / "sample_data"
        / "job_descriptions"
        / "redrob_ai_engineer.txt"
    )

    jd = job_path.read_text(encoding="utf8")

    parsed = parser.parse(jd)

    print("\n" + "=" * 80)
    print("PARSED JOB")
    print("=" * 80)

    print(parsed.model_dump_json(indent=4))


if __name__ == "__main__":
    main()