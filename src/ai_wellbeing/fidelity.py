"""Fidelity metrics for PAIV-style LLM simulation evaluation.

The functions in this module intentionally avoid heavy dependencies. They are
small baseline metrics that make early analyses reproducible and easy to audit.
"""

from __future__ import annotations

from collections import defaultdict
from math import log, sqrt
from statistics import mean
from typing import Iterable, Mapping, Optional, Sequence, Union


Number = Union[int, float]


def _as_float_list(values: Iterable[Number], *, name: str) -> list[float]:
    converted = [float(value) for value in values]
    if not converted:
        raise ValueError(f"{name} must contain at least one value.")
    return converted


def _sample_variance(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    center = mean(values)
    return sum((value - center) ** 2 for value in values) / (len(values) - 1)


def mean_fidelity(human: Iterable[Number], model: Iterable[Number]) -> dict[str, float]:
    """Compare model and human means."""

    human_values = _as_float_list(human, name="human")
    model_values = _as_float_list(model, name="model")
    human_mean = mean(human_values)
    model_mean = mean(model_values)
    return {
        "human_mean": human_mean,
        "model_mean": model_mean,
        "absolute_difference": abs(model_mean - human_mean),
        "signed_difference": model_mean - human_mean,
    }


def variance_fidelity(human: Iterable[Number], model: Iterable[Number]) -> dict[str, Optional[float]]:
    """Compare model and human variance."""

    human_values = _as_float_list(human, name="human")
    model_values = _as_float_list(model, name="model")
    human_variance = _sample_variance(human_values)
    model_variance = _sample_variance(model_values)
    ratio = None if human_variance == 0 else model_variance / human_variance
    return {
        "human_variance": human_variance,
        "model_variance": model_variance,
        "model_to_human_ratio": ratio,
        "absolute_difference": abs(model_variance - human_variance),
    }


def wasserstein_distance_1d(human: Iterable[Number], model: Iterable[Number]) -> float:
    """Return a simple empirical 1D Wasserstein distance.

    For unequal sample sizes, values are compared at shared empirical quantile
    positions. This keeps the implementation dependency-free while preserving
    the intuition of distance between sorted distributions.
    """

    human_values = sorted(_as_float_list(human, name="human"))
    model_values = sorted(_as_float_list(model, name="model"))
    n = max(len(human_values), len(model_values))

    def quantile(sorted_values: Sequence[float], index: int) -> float:
        if n == 1:
            return sorted_values[0]
        position = index * (len(sorted_values) - 1) / (n - 1)
        lower = int(position)
        upper = min(lower + 1, len(sorted_values) - 1)
        weight = position - lower
        return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight

    return sum(abs(quantile(human_values, i) - quantile(model_values, i)) for i in range(n)) / n


def histogram_kl_divergence(
    human: Iterable[Number],
    model: Iterable[Number],
    *,
    bins: int = 10,
    epsilon: float = 1e-12,
) -> float:
    """Approximate KL(human || model) with equal-width histograms."""

    if bins < 1:
        raise ValueError("bins must be at least 1.")
    human_values = _as_float_list(human, name="human")
    model_values = _as_float_list(model, name="model")
    lower = min(min(human_values), min(model_values))
    upper = max(max(human_values), max(model_values))
    if lower == upper:
        return 0.0
    width = (upper - lower) / bins

    def counts(values: Sequence[float]) -> list[int]:
        output = [0] * bins
        for value in values:
            index = min(int((value - lower) / width), bins - 1)
            output[index] += 1
        return output

    human_counts = counts(human_values)
    model_counts = counts(model_values)
    human_total = sum(human_counts) + epsilon * bins
    model_total = sum(model_counts) + epsilon * bins
    divergence = 0.0
    for human_count, model_count in zip(human_counts, model_counts):
        p = (human_count + epsilon) / human_total
        q = (model_count + epsilon) / model_total
        divergence += p * log(p / q)
    return divergence


def distribution_fidelity(
    human: Iterable[Number],
    model: Iterable[Number],
    *,
    bins: int = 10,
) -> dict[str, float]:
    """Compare full response distributions."""

    human_values = _as_float_list(human, name="human")
    model_values = _as_float_list(model, name="model")
    return {
        "wasserstein_distance": wasserstein_distance_1d(human_values, model_values),
        "histogram_kl_divergence": histogram_kl_divergence(human_values, model_values, bins=bins),
    }


def identity_fidelity(
    human: Sequence[Mapping[str, object]],
    model: Sequence[Mapping[str, object]],
    *,
    group_key: str,
    score_key: str,
) -> dict[str, dict[str, float]]:
    """Compare human and model means within identity groups."""

    human_groups = _group_scores(human, group_key=group_key, score_key=score_key)
    model_groups = _group_scores(model, group_key=group_key, score_key=score_key)
    shared_groups = sorted(set(human_groups).intersection(model_groups))
    if not shared_groups:
        raise ValueError("human and model records do not share any identity groups.")
    return {
        group: mean_fidelity(human_groups[group], model_groups[group])
        for group in shared_groups
    }


def behavioral_fidelity(
    human: Sequence[Mapping[str, object]],
    model: Sequence[Mapping[str, object]],
    *,
    wellbeing_key: str,
    behavior_key: str,
) -> dict[str, Optional[float]]:
    """Compare well-being/behavior correlations in human and model records."""

    human_pairs = _paired_scores(human, x_key=wellbeing_key, y_key=behavior_key)
    model_pairs = _paired_scores(model, x_key=wellbeing_key, y_key=behavior_key)
    human_correlation = _pearson(human_pairs)
    model_correlation = _pearson(model_pairs)
    difference = None
    if human_correlation is not None and model_correlation is not None:
        difference = model_correlation - human_correlation
    return {
        "human_correlation": human_correlation,
        "model_correlation": model_correlation,
        "signed_difference": difference,
        "absolute_difference": None if difference is None else abs(difference),
    }


def fidelity_report(
    human: Iterable[Number],
    model: Iterable[Number],
    *,
    bins: int = 10,
) -> dict[str, dict[str, Optional[float]]]:
    """Return a compact report for the core score-level fidelity layers."""

    human_values = _as_float_list(human, name="human")
    model_values = _as_float_list(model, name="model")
    return {
        "mean_fidelity": mean_fidelity(human_values, model_values),
        "variance_fidelity": variance_fidelity(human_values, model_values),
        "distribution_fidelity": distribution_fidelity(human_values, model_values, bins=bins),
    }


def _group_scores(
    records: Sequence[Mapping[str, object]],
    *,
    group_key: str,
    score_key: str,
) -> dict[str, list[float]]:
    groups: dict[str, list[float]] = defaultdict(list)
    for record in records:
        group = record.get(group_key)
        score = record.get(score_key)
        if group is None or score is None:
            continue
        groups[str(group)].append(float(score))
    return dict(groups)


def _paired_scores(
    records: Sequence[Mapping[str, object]],
    *,
    x_key: str,
    y_key: str,
) -> list[tuple[float, float]]:
    pairs: list[tuple[float, float]] = []
    for record in records:
        x = record.get(x_key)
        y = record.get(y_key)
        if x is None or y is None:
            continue
        pairs.append((float(x), float(y)))
    return pairs


def _pearson(pairs: Sequence[tuple[float, float]]) -> Optional[float]:
    if len(pairs) < 2:
        return None
    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in pairs)
    x_ss = sum((x - x_mean) ** 2 for x in xs)
    y_ss = sum((y - y_mean) ** 2 for y in ys)
    denominator = sqrt(x_ss * y_ss)
    if denominator == 0:
        return None
    return numerator / denominator
