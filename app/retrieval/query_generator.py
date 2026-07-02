from app.kg.query_expander import QueryExpander
from app.retrieval.search_query import SearchQuery


class QueryGenerator:

    def __init__(self):

        self.expander = QueryExpander()

    # =====================================================
    # Main API
    # =====================================================

    def generate(self, parsed_job, hyre):

        positive = self.generate_positive(hyre)

        negative = self.generate_negative(hyre)

        return positive + negative

    # =====================================================
    # Positive Queries
    # =====================================================

    def generate_positive(self, hyre):

        queries = []

        # Skills
        for skill in hyre.skills:

            queries.append(

                SearchQuery(

                    text=skill,

                    weight=1.0,

                    query_type="positive",

                    category="skill",

                    sources=["HYRE Skill"],

                )

            )

        # Technologies
        for tech in hyre.technologies:

            queries.append(

                SearchQuery(

                    text=tech,

                    weight=0.95,

                    query_type="positive",

                    category="technology",

                    sources=["HYRE Technology"],

                )

            )

        # Titles
        for title in hyre.target_titles:

            queries.append(

                SearchQuery(

                    text=title,

                    weight=1.0,

                    query_type="positive",

                    category="title",

                    sources=["HYRE Title"],

                )

            )

        # Search Keywords
        for keyword in hyre.search_keywords:

            queries.append(

                SearchQuery(

                    text=keyword,

                    weight=0.90,

                    query_type="positive",

                    category="keyword",

                    sources=["HYRE Keyword"],

                )

            )

        # Positive Queries
        for query in hyre.positive_queries:

            queries.append(

                SearchQuery(

                    text=query,

                    weight=0.85,

                    query_type="positive",

                    category="query",

                    sources=["HYRE Query"],

                )

            )

        # Knowledge Graph Expansion
        expanded = self.expander.expand(hyre)

        for entity in expanded:

            queries.append(

                SearchQuery(

                    text=entity,

                    weight=0.75,

                    query_type="positive",

                    category="knowledge_graph",

                    sources=["Knowledge Graph"],

                )

            )

        return self._merge(queries)

    # =====================================================
    # Negative Queries
    # =====================================================

    def generate_negative(self, hyre):

        queries = []

        for query in hyre.negative_queries:

            queries.append(

                SearchQuery(

                    text=query,

                    weight=1.0,

                    query_type="negative",

                    category="negative",

                    sources=["HYRE Negative"],

                )

            )

        return self._merge(queries)

    # =====================================================
    # Normalize
    # =====================================================

    def _normalize(self, text: str):

        mapping = {

            "sentence-transformers": "Sentence Transformers",
            "sentence transformers": "Sentence Transformers",

            "llm": "LLMs",
            "large language model": "LLMs",
            "large language models": "LLMs",
            "large language models (llms)": "LLMs",

            "vector db": "Vector Databases",
            "vector database": "Vector Databases",
            "vector databases": "Vector Databases",

            "learning to rank": "Learning-to-Rank",
            "learning-to-rank": "Learning-to-Rank",

            "retrieval system": "Retrieval",
            "retrieval systems": "Retrieval",

            "ranking system": "Ranking",
            "ranking systems": "Ranking",

        }

        key = text.lower().strip()

        return mapping.get(key, text)

    # =====================================================
    # Merge
    # =====================================================

    def _merge(self, queries):

        merged = {}

        for query in queries:

            query.text = self._normalize(query.text)

            key = query.text.lower().strip()

            if key not in merged:

                merged[key] = query

            else:

                merged[key].weight += query.weight

                for source in query.sources:

                    if source not in merged[key].sources:

                        merged[key].sources.append(source)

        return sorted(

            merged.values(),

            key=lambda q: q.weight,

            reverse=True,

        )