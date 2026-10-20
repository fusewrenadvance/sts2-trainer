# Contributing to sts2-trainer

Thanks for poking at the trainer. This is a hobbyist project — a Slay the Spire 2
trainer that hooks the Steam build via a read/write memory layer plus a small
overlay for hotkey feedback.

## Ground rules

- Trainer targets the **single-player Steam build** of Slay the Spire 2 only.
  No online, no co-op, no leaderboard submission.
- Every feature module must declare its offsets in `config/offsets.yaml` and
  degrade gracefully if a signature scan fails (log + disable, never crash).
- Don't hardcode addresses. Use `offsets/` + `utils/memory.py` resolvers.
- Keep the overlay optional. The trainer must run headless (`--no-overlay`).

## Workflow

1. Fork, branch off `main` (`feat/energy-lock`, `fix/gold-overflow`, ...).
2. Run `pytest tests/` before opening a PR.
3. Update `config/offsets.yaml` if you touched a signature.
4. Add a line to `CHANGELOG.md` under *Unreleased*.

## Style

- Python 3.11, `ruff` + `black` defaults.
- Small modules. One feature = one file under `src/sts2_trainer/features/`.
- Log with `loguru`-style `logger.info(...)` from `utils.logger`.

## Reporting broken offsets

Open an issue with the `offset-drift` label and paste the output of:

```
python -m sts2_trainer.cli scan --verbose
```