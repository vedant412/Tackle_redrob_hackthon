from enum import Enum


class QueryCategory(str, Enum):

    SKILL = "skill"

    TECHNOLOGY = "technology"

    TITLE = "title"

    KEYWORD = "keyword"

    QUERY = "query"

    KNOWLEDGE_GRAPH = "knowledge_graph"

    NEGATIVE = "negative"