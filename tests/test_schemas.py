import unittest

from ai_wellbeing.schemas import validate_benchmark_record, validate_simulation_record


class SchemaValidationTests(unittest.TestCase):
    def test_validate_benchmark_record_accepts_minimal_record(self):
        validate_benchmark_record(
            {
                "participant_id": "p001",
                "construct": "life_satisfaction",
                "score": 6.0,
                "instrument": "SWLS",
            }
        )

    def test_validate_benchmark_record_rejects_missing_score(self):
        with self.assertRaisesRegex(ValueError, "score"):
            validate_benchmark_record(
                {
                    "participant_id": "p001",
                    "construct": "life_satisfaction",
                    "instrument": "SWLS",
                }
            )

    def test_validate_simulation_record_accepts_minimal_record(self):
        validate_simulation_record(
            {
                "simulation_id": "s001",
                "model": "example-model",
                "construct": "life_satisfaction",
                "score": 5.0,
                "prompt_id": "swls-v1",
            }
        )

    def test_validate_simulation_record_rejects_boolean_score(self):
        with self.assertRaisesRegex(ValueError, "score"):
            validate_simulation_record(
                {
                    "simulation_id": "s001",
                    "model": "example-model",
                    "construct": "life_satisfaction",
                    "score": True,
                    "prompt_id": "swls-v1",
                }
            )


if __name__ == "__main__":
    unittest.main()
