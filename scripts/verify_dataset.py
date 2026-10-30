"""Run twice, validate independently, compare every exported byte, package proof."""
import argparse
import json
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from integrity.dataset import canonical, generate, negative_fixtures, write_exports, SEED, GENERATOR_VERSION
from integrity.validation import evaluate

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["full", "starter"], default="full")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "reproducibility")
    parser.add_argument("--package", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    manifests = [write_exports(args.output / name, args.mode, SEED) for name in ["run-a", "run-b"]]
    data, truth = generate(args.mode, SEED)
    fixtures = negative_fixtures(data)
    negative_truth = [{"fixture_id": f["fixture_id"], "expected_detection": f["fixture_id"]} for f in fixtures]
    report = evaluate(data, truth, fixtures, negative_truth, args.mode)
    report["reproducibility"] = {"generator_version": GENERATOR_VERSION, "seed": SEED, "mode": args.mode, "counts_match": manifests[0]["counts"] == manifests[1]["counts"],
        "all_checksums_match": manifests[0]["sha256"] == manifests[1]["sha256"], "sha256": manifests[0]["sha256"]}
    report["execution"] = {"ran_at_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
                           "elapsed_seconds": round(time.perf_counter() - started, 3)}
    report["passed"] = report["passed"] and report["reproducibility"]["all_checksums_match"] and report["reproducibility"]["counts_match"]
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "verification.json").write_text(canonical(report), encoding="utf-8", newline="\n")
    if args.package:
        destination = ROOT / "data"
        destination.mkdir(exist_ok=True)
        with zipfile.ZipFile(destination / f"{args.mode}-dataset.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted((args.output / "run-a").iterdir()):
                info = zipfile.ZipInfo(path.name, (2026, 9, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
        (destination / "verification.json").write_text(canonical(report), encoding="utf-8", newline="\n")
    print(json.dumps({"passed": report["passed"], "baseline_errors": len(report["baseline_findings"]),
        "detection": report["detection_confusion"], "checksums_match": report["reproducibility"]["all_checksums_match"],
        "elapsed_seconds": report["execution"]["elapsed_seconds"]}, indent=2))
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
