import json
from pathlib import Path

from app.models import ParsedJob


class LLMJobParser:

    def __init__(self, provider):

        self.provider = provider

        prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "job_parser_prompt.txt"
        )

        self.prompt_template = prompt_path.read_text(
            encoding="utf8"
        )

    # ---------------------------------------------------------

    def parse(self, job_description: str) -> ParsedJob:

        prompt = self.prompt_template.replace(
            "{{JOB_DESCRIPTION}}",
            job_description,
        )

        response = self.provider.generate(
            prompt=prompt,
            response_schema=ParsedJob,
        )

        # --------------------------------------------
        # Provider Response Handling
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
        # Normalize Provider Output
        # --------------------------------------------

        data = self._normalize(data)

        return ParsedJob.model_validate(data)

    # ---------------------------------------------------------

    def _normalize(self, data: dict) -> dict:

        # --------------------------------------------
        # Fields expected as list[str]
        # --------------------------------------------

        list_fields = [

            "required_skills",
            "preferred_skills",
            "excluded_skills",

            "education",
            "certifications",

            "industries",
            "preferred_companies",
            "excluded_companies",

            "preferred_locations",

            "must_have",
            "nice_to_have",
            "hard_constraints",

            "avoid_backgrounds",
            "avoid_industries",
            "avoid_titles",
            "negative_keywords",

            "behavioural_traits",
            "culture_fit",

            "hiring_priorities",
            "recruiter_preferences",

            "positive_queries",
            "negative_queries",
            "kg_entities",

        ]

        for field in list_fields:

            value = data.get(field)

            if value is None:

                data[field] = []

                continue

            # Convert dict -> list
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

            # Convert scalar -> list
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
        # String fields
        # --------------------------------------------

        string_fields = [

            "title",
            "summary",
            "seniority",
            "employment_type",
            "work_mode",
            "ideal_candidate_summary",

        ]

        for field in string_fields:

            value = data.get(field)

            if value is None:

                continue

            if not isinstance(value, str):

                data[field] = str(value)

        # --------------------------------------------
        # Numeric fields
        # --------------------------------------------

        int_fields = [

            "minimum_experience",
            "maximum_experience",

        ]

        for field in int_fields:

            value = data.get(field)

            if value in (None, ""):

                continue

            try:

                data[field] = int(value)

            except Exception:

                data[field] = None

        float_fields = [

            "salary_min",
            "salary_max",

        ]

        for field in float_fields:

            value = data.get(field)

            if value in (None, ""):

                continue

            try:

                data[field] = float(value)

            except Exception:

                data[field] = None

        return data