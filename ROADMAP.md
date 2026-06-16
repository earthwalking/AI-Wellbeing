# Roadmap

AI-Wellbeing is organized around the Psychological AI Validity Framework (PAIV).
The roadmap prioritizes small, auditable releases that make LLM simulation
claims easier to reproduce and challenge.

## 0.1 Seed Release

- [x] Public repository skeleton
- [x] MIT license
- [x] PAIV-oriented README
- [x] Human benchmark JSON schema
- [x] LLM simulation JSON schema
- [x] Mean, variance, distribution, identity, and behavioral fidelity helpers
- [x] Minimal tests

## 0.2 Benchmark Templates

- [ ] Add well-being benchmark variable dictionary
- [ ] Add prompt metadata template
- [ ] Add non-sensitive example dataset
- [ ] Add CLI command for validating benchmark and simulation files
- [ ] Add report template for PAIV fidelity summaries

## 0.3 Multi-Model Simulation Workflow

- [ ] Add experiment manifest format
- [ ] Add model-output normalization utilities
- [ ] Add deterministic sampling and stratification helpers
- [ ] Add reproducible run logs for model, prompt, seed, and date metadata
- [ ] Add example notebook comparing multiple model families

## 0.4 Psychometric Validity Layer

- [ ] Add construct metadata schema
- [ ] Add item-level scoring helpers
- [ ] Add reliability and dimensionality checks
- [ ] Add measurement-invariance reporting template
- [ ] Add documentation for separating construct validity from simulation fidelity

## 0.5 Research Release

- [ ] Add manuscript-aligned analysis scripts
- [ ] Add human benchmark documentation for public or shareable data only
- [ ] Add package documentation site
- [ ] Add contribution guide
- [ ] Tag first citable release

## Design Principles

- Prefer transparent metrics over opaque scores.
- Compare distributions, not only averages.
- Treat subgroup and behavioral distortions as first-class evidence.
- Keep private or sensitive human data outside the repository.
- Make every reported simulation result traceable to model, prompt, schema, and
  analysis version.
