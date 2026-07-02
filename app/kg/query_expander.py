from app.kg.kg_service import KnowledgeGraphService


class QueryExpander:

    def __init__(self):

        self.kg = KnowledgeGraphService()

    def expand(self, hyre):

        expanded = set()

        expanded.update(

            self.kg.expand(hyre.skills)

        )

        expanded.update(

            self.kg.expand(hyre.technologies)

        )

        return sorted(set(expanded))