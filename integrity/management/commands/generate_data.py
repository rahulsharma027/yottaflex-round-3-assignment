from django.core.management.base import BaseCommand
from integrity.dataset import SEED, write_exports

class Command(BaseCommand):
    help = "Export deterministic CSV, JSON and standalone SQLite SQL, with separate truth and negative fixtures."
    def add_arguments(self, parser):
        parser.add_argument("--mode", choices=["full", "starter"], default="full")
        parser.add_argument("--seed", type=int, default=SEED)
        parser.add_argument("--output", required=True)
    def handle(self, *args, **options):
        manifest = write_exports(options["output"], options["mode"], options["seed"])
        self.stdout.write(f"Exported {manifest['mode']}: {manifest['counts']['submission']} submissions; {manifest['flagged_reports']} flags; {manifest['counts']['case']} cases.")
