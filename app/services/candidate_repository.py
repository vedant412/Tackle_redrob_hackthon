from pathlib import Path

from app.models.candidate import Candidate
from app.services.data_loader import DataLoader


class CandidateRepository:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._initialized = False

        return cls._instance

    def __init__(self):

        if self._initialized:
            return

        self._candidates: list[Candidate] = []

        self._candidate_map: dict[str, Candidate] = {}

        self._initialized = True

    def load(self, file_path: str | Path):

        if self._candidates:
            return

        print("Loading candidate repository...")

        self._candidates = DataLoader.load_candidates(file_path)

        self._candidate_map = {
            c.candidate_id: c
            for c in self._candidates
        }

        print(f"Loaded {len(self._candidates)} candidates.")

    def get_candidate(self, candidate_id: str):

        return self._candidate_map.get(candidate_id)

    def get_candidates(self, candidate_ids):

        return [

            self._candidate_map[cid]

            for cid in candidate_ids

            if cid in self._candidate_map

        ]

    def get_all(self):

        return self._candidates

    def count(self):

        return len(self._candidates)

    def exists(self, candidate_id):

        return candidate_id in self._candidate_map