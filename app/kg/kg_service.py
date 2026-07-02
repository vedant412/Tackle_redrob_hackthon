from app.kg.ontology import KG


class KnowledgeGraphService:

    def expand(self, entities: list[str]) -> list[str]:

        expanded = set()

        for entity in entities:

            expanded.add(entity.strip())

            node = KG.get(entity)

            if not node:
                continue

            expanded.update(x.strip() for x in node.get("aliases", []))
            expanded.update(x.strip() for x in node.get("children", []))
            expanded.update(x.strip() for x in node.get("related", []))
        return sorted(expanded)