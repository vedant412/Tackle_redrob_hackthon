from pathlib import Path

import pandas as pd


class CSVExporter:

    def export(
        self,
        explanations,
        output_path,
        top_k: int = 100,
    ):

        # ----------------------------------------
        # Keep only Top K
        # ----------------------------------------

        explanations = sorted(
            explanations,
            key=lambda x: x.final_score,
            reverse=True,
        )[:top_k]

        rows = []

        for rank, candidate in enumerate(explanations, start=1):

            rows.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "rank": rank,
                    "score": round(float(candidate.final_score), 6),
                    "reasoning": candidate.reasoning,
                }
            )

        df = pd.DataFrame(rows)

        # ----------------------------------------
        # Validation
        # ----------------------------------------

        assert len(df) == top_k, (
            f"Expected {top_k} candidates, got {len(df)}"
        )

        assert df["rank"].tolist() == list(range(1, top_k + 1))

        assert df["score"].is_monotonic_decreasing

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            output_path,
            index=False,
        )

        print("=" * 80)
        print("SUBMISSION FILE CREATED")
        print("=" * 80)
        print(f"Saved {top_k} candidates")
        print(output_path)

        return df