# Packaged synthetic data

`full-dataset.zip` is produced by `python scripts/verify_dataset.py --package`. It contains full CSV/JSON/SQLite SQL, separate truth, four isolated invalid fixtures and a source/checksum manifest. `verification.json` records actual validation and two-run proof. Compression avoids tens of megabytes of repeated text in Git.

Extract before inspecting individual files. The launcher uses the same generator but never imports truth or invalid fixtures. See docs/DATASET.md for exact assumptions and formats.
