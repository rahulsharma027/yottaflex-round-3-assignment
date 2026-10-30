# Packaged synthetic data

Current package: **generator revision 2**, seed **20261022**, 10,000 submissions / 1,000 flags / 300 cases. Academic originals omit future process findings; scenarios and assessments use separate seeded shuffled plans. `manifest.json` records the revision and each file hash.

`verification.json` was regenerated on Python 3.12; `python314-verification.json` records the Python 3.14 run. Exported file hashes match across these tested runtimes. `scenario_distribution` describes assessment/scenario mixing and mixed learner outcomes, without claiming real-world detection accuracy.

`full-dataset.zip` is produced by `python scripts/verify_dataset.py --package`. It contains full CSV/JSON/SQLite SQL, separate truth, four isolated invalid fixtures and a source/checksum manifest. `verification.json` records actual validation and two-run proof. Compression avoids tens of megabytes of repeated text in Git.

Extract before inspecting individual files. The launcher uses the same generator but never imports truth or invalid fixtures. Existing workspaces are preserved; use the separate-workspace instructions in [README](../README.md) to inspect refreshed data. See [DATASET.md](../docs/DATASET.md) for exact assumptions and formats.
