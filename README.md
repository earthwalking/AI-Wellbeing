# AI-Wellbeing

Open-source tools for evaluating psychological validity in large language model
simulations of human well-being.

AI-Wellbeing implements the **Psychological AI Validity Framework (PAIV)**: a
research workflow for asking when AI-generated responses preserve meaningful
human psychological structure, and when they only look plausible at the surface.

The project is early-stage and is being developed alongside an active PhD
research program on LLM simulation validity, human benchmark validity, and
well-being measurement.

## Why This Exists

LLMs are increasingly used as simulated participants, human surrogates, and
behavioral reasoning systems. Mean-level similarity is not enough to support
psychological claims. A model can match a group average while compressing human
variance, distorting subgroup patterns, or breaking relationships between
well-being and behavior.

AI-Wellbeing turns that problem into a reproducible open-source workflow:

1. Define a human benchmark schema.
2. Collect or import model simulation outputs.
3. Compare human and model responses across multiple fidelity layers.
4. Report where psychological structure is preserved, compressed, or distorted.

## PAIV Framework

The current implementation focuses on five simulation-validity layers:

| Layer | Question | Example metric |
| --- | --- | --- |
| Mean fidelity | Does the model match human group averages? | Absolute mean difference |
| Variance fidelity | Does the model preserve human heterogeneity? | Variance ratio |
| Distribution fidelity | Does the model match the full response distribution? | 1D Wasserstein distance, histogram KL divergence |
| Identity fidelity | Does the model preserve subgroup patterns? | Group-wise mean differences |
| Behavioral fidelity | Does the model preserve behavioral ecology? | Correlation differences |

## Repository Layout

```text
AI-Wellbeing/
  README.md
  LICENSE
  ROADMAP.md
  pyproject.toml
  schemas/
    benchmark.schema.json
    simulation.schema.json
  src/ai_wellbeing/
    __init__.py
    fidelity.py
    schemas.py
  tests/
    test_fidelity.py
    test_schemas.py
```

## Quick Start

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

Minimal example:

```python
from ai_wellbeing.fidelity import fidelity_report

human_scores = [4, 5, 6, 7, 6, 5, 4]
model_scores = [5, 5, 6, 6, 6, 5, 5]

report = fidelity_report(human_scores, model_scores)
print(report["mean_fidelity"]["absolute_difference"])
print(report["variance_fidelity"]["model_to_human_ratio"])
```

## Data Policy

This repository is intended to publish reusable code, schemas, prompts, and
non-sensitive benchmark templates. Human participant data should not be committed
unless it is public, consented, de-identified, and license-compatible.

## Current Status

This is a seed release. The first milestone is a transparent, tested baseline for
PAIV-style fidelity metrics. Future releases will add richer psychometric
validity checks, prompt templates, multi-model experiment runners, and example
notebooks.

See [ROADMAP.md](ROADMAP.md) for planned work.

## Citation

If you use this project in academic work, cite the repository for now:

```text
Ke, L. (2026). AI-Wellbeing: Open-source tools for psychological AI validity
and LLM well-being simulation fidelity. GitHub.
https://github.com/earthwalking/AI-Wellbeing
```

## License

MIT License. See [LICENSE](LICENSE).
