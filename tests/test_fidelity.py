import unittest

from ai_wellbeing.fidelity import (
    behavioral_fidelity,
    distribution_fidelity,
    fidelity_report,
    identity_fidelity,
    mean_fidelity,
    variance_fidelity,
)


class FidelityMetricTests(unittest.TestCase):
    def test_mean_fidelity_reports_signed_and_absolute_difference(self):
        report = mean_fidelity([1, 2, 3], [2, 3, 4])

        self.assertEqual(report["human_mean"], 2)
        self.assertEqual(report["model_mean"], 3)
        self.assertEqual(report["signed_difference"], 1)
        self.assertEqual(report["absolute_difference"], 1)


    def test_variance_fidelity_detects_compression(self):
        report = variance_fidelity([1, 3, 5], [2, 3, 4])

        self.assertEqual(report["human_variance"], 4)
        self.assertEqual(report["model_variance"], 1)
        self.assertEqual(report["model_to_human_ratio"], 0.25)


    def test_distribution_fidelity_is_zero_for_identical_samples(self):
        report = distribution_fidelity([1, 2, 3], [1, 2, 3], bins=3)

        self.assertEqual(report["wasserstein_distance"], 0)
        self.assertEqual(report["histogram_kl_divergence"], 0)


    def test_identity_fidelity_reports_shared_groups(self):
        human = [
            {"gender": "women", "score": 5},
            {"gender": "women", "score": 7},
            {"gender": "men", "score": 4},
        ]
        model = [
            {"gender": "women", "score": 6},
            {"gender": "men", "score": 6},
        ]

        report = identity_fidelity(human, model, group_key="gender", score_key="score")

        self.assertEqual(report["women"]["absolute_difference"], 0)
        self.assertEqual(report["men"]["absolute_difference"], 2)


    def test_behavioral_fidelity_compares_correlations(self):
        human = [
            {"wellbeing": 1, "trust": 1},
            {"wellbeing": 2, "trust": 2},
            {"wellbeing": 3, "trust": 3},
        ]
        model = [
            {"wellbeing": 1, "trust": 3},
            {"wellbeing": 2, "trust": 2},
            {"wellbeing": 3, "trust": 1},
        ]

        report = behavioral_fidelity(
            human,
            model,
            wellbeing_key="wellbeing",
            behavior_key="trust",
        )

        self.assertEqual(report["human_correlation"], 1)
        self.assertEqual(report["model_correlation"], -1)
        self.assertEqual(report["absolute_difference"], 2)


    def test_fidelity_report_contains_core_layers(self):
        report = fidelity_report([1, 2, 3], [1, 2, 2], bins=3)

        self.assertEqual(
            set(report),
            {
                "mean_fidelity",
                "variance_fidelity",
                "distribution_fidelity",
            },
        )


if __name__ == "__main__":
    unittest.main()
