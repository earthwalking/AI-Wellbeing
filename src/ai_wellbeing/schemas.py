"""Lightweight record schemas for PAIV benchmark and simulation data."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class IdentityAttributes:
    """Optional participant or persona attributes used for subgroup fidelity."""

    gender: Optional[str] = None
    age_group: Optional[str] = None
    education: Optional[str] = None
    income_group: Optional[str] = None
    region: Optional[str] = None


@dataclass(frozen=True)
class BenchmarkRecord:
    """A de-identified human benchmark observation."""

    participant_id: str
    construct: str
    score: float
    instrument: str
    identity: IdentityAttributes = field(default_factory=IdentityAttributes)
    behavior: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SimulationRecord:
    """A model-generated observation aligned to a benchmark construct."""

    simulation_id: str
    model: str
    construct: str
    score: float
    prompt_id: str
    persona: IdentityAttributes = field(default_factory=IdentityAttributes)
    behavior: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


def validate_benchmark_record(record: Mapping[str, Any]) -> None:
    """Validate the minimal required fields for a benchmark record."""

    _require_string(record, "participant_id")
    _require_string(record, "construct")
    _require_number(record, "score")
    _require_string(record, "instrument")
    _require_optional_mapping(record, "identity")
    _require_optional_mapping(record, "behavior")
    _require_optional_mapping(record, "metadata")


def validate_simulation_record(record: Mapping[str, Any]) -> None:
    """Validate the minimal required fields for a simulation record."""

    _require_string(record, "simulation_id")
    _require_string(record, "model")
    _require_string(record, "construct")
    _require_number(record, "score")
    _require_string(record, "prompt_id")
    _require_optional_mapping(record, "persona")
    _require_optional_mapping(record, "behavior")
    _require_optional_mapping(record, "metadata")


def _require_string(record: Mapping[str, Any], key: str) -> None:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string.")


def _require_number(record: Mapping[str, Any], key: str) -> None:
    value = record.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{key} must be a number.")


def _require_optional_mapping(record: Mapping[str, Any], key: str) -> None:
    value = record.get(key)
    if value is not None and not isinstance(value, Mapping):
        raise ValueError(f"{key} must be an object when provided.")
