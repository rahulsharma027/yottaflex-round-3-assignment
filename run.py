"""One-command, non-destructive local launcher; standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent

def execute(arguments, env=None):
    subprocess.run([str(arg) for arg in arguments], cwd=ROOT, env=env, check=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--mode", choices=["full", "starter"], default="full", help="Applies only to an empty database.")
    parser.add_argument("--setup-only", action="store_true")
    parser.add_argument("--reset-demo", action="store_true", help="Requires --confirm-reset; removes only the local demo database and generated account passwords.")
    parser.add_argument("--confirm-reset", action="store_true")
    args = parser.parse_args()
    if not (3, 12) <= sys.version_info[:2] <= (3, 15):
        parser.error("Use Python 3.12–3.14 (recommended). Python 3.15 is experimental with this Django pin.")
    if sys.version_info[:2] == (3, 15):
        print("Note: Python 3.15 is experimental with Django 5.2. Prefer Python 3.12–3.14.", flush=True)
    if not 1 <= args.port <= 65535:
        parser.error("Port must be between 1 and 65535.")
    if args.reset_demo and not args.confirm_reset:
        parser.error("Reset deletes local reviewer changes. Add --confirm-reset deliberately, or use a new YOTTA_LOCAL_DIR.")
    if not args.setup_only:
        try:
            with socket.socket() as probe:
                probe.bind(("127.0.0.1", args.port))
        except OSError:
            parser.error(f"Port {args.port} is occupied. Try python run.py --port {args.port+1}.")
    local = Path(os.environ.get("YOTTA_LOCAL_DIR", ROOT / ".local")).resolve()
    local.mkdir(parents=True, exist_ok=True)
    if args.reset_demo:
        # Explicit, fixed filenames only; no recursive deletion or guessed paths.
        for filename in ["yotta.sqlite3", "yotta.sqlite3-wal", "yotta.sqlite3-shm", "demo-accounts.json"]:
            (local / filename).unlink(missing_ok=True)
    env_path = ROOT / ".venv"
    python = env_path / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        print("Creating isolated Python environment…", flush=True)
        venv.EnvBuilder(with_pip=True).create(env_path)
    dependency_hash = hashlib.sha256((ROOT / "requirements.txt").read_bytes()).hexdigest()
    marker = env_path / ".requirements-sha256"
    if not marker.exists() or marker.read_text() != dependency_hash:
        print("Installing pinned dependencies (internet needed on first run)…", flush=True)
        execute([python, "-m", "pip", "install", "--disable-pip-version-check", "-r", ROOT / "requirements.txt"])
        marker.write_text(dependency_hash)
    env = os.environ.copy()
    env["YOTTA_LOCAL_DIR"] = str(local)
    execute([python, "manage.py", "migrate", "--noinput"], env)
    execute([python, "manage.py", "seed_demo", "--mode", args.mode], env)
    credentials = json.loads((local / "demo-accounts.json").read_text(encoding="utf-8"))
    print("\nYotta / local synthetic workspace\n", flush=True)
    for username, password in credentials.items():
        print(f"  {username:18} {password}", flush=True)
    print(f"\nCredentials: {local / 'demo-accounts.json'} (keep private)\n", flush=True)
    if not args.setup_only:
        print(f"Open http://127.0.0.1:{args.port}/  |  Stop with Ctrl+C\n", flush=True)
        execute([python, "manage.py", "runserver", f"127.0.0.1:{args.port}", "--noreload", "--insecure"], env)
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nYotta stopped. Your data is preserved.")
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"\nSetup could not finish: {exc}\nFix the error above and rerun the same command; existing data is preserved.", file=sys.stderr)
        raise SystemExit(1)
