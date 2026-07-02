import json
from pathlib import Path

from app.models import HYREProfile


class HYREGenerator:

    def __init__(self, provider):

        self.provider = provider

        prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "hyre_prompt.txt"
        )

        self.prompt_template = prompt_path.read_text(
            encoding="utf8"
        )

    # ---------------------------------------------------------

    def generate(self, parsed_job) -> HYREProfile:

        prompt = (
            self.prompt_template
            + "\n\n"
            + parsed_job.model_dump_json(indent=2)
        )

        response = self.provider.generate(
            prompt=prompt,
            response_schema=HYREProfile,
        )

        # --------------------------------------------
        # Provider Response
        # --------------------------------------------

        if hasattr(response, "parsed"):

            data = response.parsed

        else:

            data = response

        if isinstance(data, str):

            data = json.loads(data)

        if not isinstance(data, dict):

            raise ValueError(
                f"Expected dict from provider, got {type(data)}"
            )

        # --------------------------------------------
        # Normalize
        # --------------------------------------------

        data = self._normalize(data)

        return HYREProfile.model_validate(data)

    # ---------------------------------------------------------

    def _normalize(self, data: dict) -> dict:

        # --------------------------------------------
        # Fields expected as list[str]
        # --------------------------------------------

        list_fields = [

            "target_titles",
            "skills",
            "technologies",
            "industries",
            "company_types",
            "preferred_companies",
            "excluded_companies",
            "education",
            "certifications",
            "locations",
            "behavioural_traits",
            "recruiter_intent",
            "positive_queries",
            "negative_queries",
            "search_keywords",

        ]

        for field in list_fields:

            value = data.get(field)

            if value is None:

                data[field] = []

                continue

            # Dict -> List
            if isinstance(value, dict):

                normalized = []

                for k, v in value.items():

                    if isinstance(v, bool):

                        if v:

                            normalized.append(str(k))

                    elif v is not None:

                        normalized.append(str(v))

                data[field] = normalized

                continue

            # Scalar -> List
            if not isinstance(value, list):

                value = [value]

            normalized = []

            for item in value:

                if item is None:

                    continue

                if isinstance(item, bool):

                    normalized.append(str(item))

                elif isinstance(item, (int, float)):

                    normalized.append(str(item))

                elif isinstance(item, dict):

                    normalized.extend(

                        str(v)

                        for v in item.values()

                        if v is not None

                    )

                else:

                    normalized.append(str(item))

            data[field] = normalized

        # --------------------------------------------
        # String Fields
        # --------------------------------------------

        string_fields = [

            "headline",
            "summary",
            "experience_years",
            "work_mode",

        ]

        for field in string_fields:

            value = data.get(field)

            if value is None:

                continue

            if not isinstance(value, str):

                data[field] = str(value)

        return data