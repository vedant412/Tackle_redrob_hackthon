import json
import logging
import time
from pathlib import Path

from app.models.candidate import Candidate

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Loads and validates candidate profiles from JSON or JSONL files.
    """

    @staticmethod
    def load_candidates(file_path: str | Path) -> list[Candidate]:
        """
        Load candidate profiles from a JSON or JSONL file.

        Parameters
        ----------
        file_path : str | Path
            Path to the candidate dataset.

        Returns
        -------
        list[Candidate]
            List of validated Candidate objects.
        """

        start_time = time.time()

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        # ---------------------------
        # Read dataset
        # ---------------------------
        with open(file_path, "r", encoding="utf-8") as f:

            if file_path.suffix == ".json":
                raw_candidates = json.load(f)

            elif file_path.suffix == ".jsonl":
                raw_candidates = [
                    json.loads(line)
                    for line in f
                    if line.strip()
                ]

            else:
                raise ValueError(
                    f"Unsupported file format: {file_path.suffix}"
                )

        # ---------------------------
        # Validate candidates
        # ---------------------------
        candidates = []
        skipped = 0

        for raw in raw_candidates:

            try:
                candidate = Candidate.model_validate(raw)
                candidates.append(candidate)

            except Exception as e:
                skipped += 1

                logger.warning(
                    "Skipping candidate %s | %s",
                    raw.get("candidate_id", "UNKNOWN"),
                    str(e)
                )

        elapsed = round(time.time() - start_time, 2)

        logger.info(
            "Loaded %d candidates | Skipped %d | Time %.2fs",
            len(candidates),
            skipped,
            elapsed
        )

        print(f" Loaded {len(candidates)} candidates")
        print(f" Skipped {skipped} invalid candidates")
        print(f" Loading Time: {elapsed} sec")

        return candidates