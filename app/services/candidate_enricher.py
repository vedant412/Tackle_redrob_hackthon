from app.services.candidate_repository import CandidateRepository


class CandidateEnricher:

    def __init__(self, repository: CandidateRepository):

        self.repository = repository

    def enrich(self, results):

        for result in results:

            result.candidate = self.repository.get_candidate(
                result.candidate_id
            )

        return results