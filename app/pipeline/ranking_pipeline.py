from app.services.llm_job_parser import LLMJobParser
from app.services.job_normalizer import JobNormalizer
from app.services.hyre_generator import HYREGenerator

from app.retrieval.query_generator import QueryGenerator
from app.retrieval.hybrid_retriever import HybridRetriever

from app.services.candidate_repository import CandidateRepository
from app.services.candidate_enricher import CandidateEnricher

from app.filtering.hard_constraint_filter import HardConstraintFilter

from app.ranking.feature_engineer import FeatureEngineer
from app.ranking.weighted_ranker import WeightedRanker

from app.explanations.explanation_generator import ExplanationGenerator
from app.exporters.csv_exporter import CSVExporter


class RankingPipeline:

    def __init__(self, provider):

        self.parser = LLMJobParser(provider)

        self.normalizer = JobNormalizer()

        self.hyre = HYREGenerator(provider)

        self.query_generator = QueryGenerator()

        self.retriever = HybridRetriever()

        self.repository = CandidateRepository()

        self.enricher = CandidateEnricher(self.repository)

        self.filter = HardConstraintFilter()

        self.feature_engineer = FeatureEngineer()

        self.ranker = WeightedRanker()

        self.explainer = ExplanationGenerator()

        self.exporter = CSVExporter()

    # -----------------------------------------------------

    def load_candidates(
        self,
        dataset_path,
    ):

        self.repository.load(
            dataset_path
        )

    # -----------------------------------------------------

    def run(

        self,

        job_description,

        output_csv="outputs/final_submission.csv",

        top_k=100,

    ):

        print("=" * 80)
        print("PARSING JOB")
        print("=" * 80)

        parsed = self.parser.parse(
            job_description
        )

        parsed = self.normalizer.normalize(
            parsed
        )

        print("=" * 80)
        print("GENERATING HYRE")
        print("=" * 80)

        hyre = self.hyre.generate(
            parsed
        )

        parsed = self.normalizer.merge_hyre(
            parsed,
            hyre,
        )

        print("=" * 80)
        print("GENERATING SEARCH QUERIES")
        print("=" * 80)

        queries = self.query_generator.generate(
            parsed,
            hyre,
        )

        print("=" * 80)
        print("HYBRID RETRIEVAL")
        print("=" * 80)

        retrieved = self.retriever.search(
            queries,
            top_k=300,
        )

        print(
            f"Retrieved : {len(retrieved)}"
        )

        print("=" * 80)
        print("ENRICHING")
        print("=" * 80)

        enriched = self.enricher.enrich(
            retrieved
        )

        print("=" * 80)
        print("FILTERING")
        print("=" * 80)

        filtered = self.filter.filter(

            enriched,

            parsed,

        )

        print(
            f"Filtered : {len(filtered)}"
        )

        print("=" * 80)
        print("FEATURE ENGINEERING")
        print("=" * 80)

        features = self.feature_engineer.build(

            filtered,

            parsed,

        )

        print("=" * 80)
        print("WEIGHTED RANKING")
        print("=" * 80)

        ranked = self.ranker.rank(

            features,

            top_k=top_k,

        )

        print("=" * 80)
        print("GENERATING EXPLANATIONS")
        print("=" * 80)

        explanations = self.explainer.generate(

            ranked,

            parsed,

        )

        print("=" * 80)
        print("EXPORTING CSV")
        print("=" * 80)

        self.exporter.export(

            explanations,

            output_csv,

            top_k=top_k,

        )

        print("=" * 80)
        print("PIPELINE COMPLETE")
        print("=" * 80)

        return explanations