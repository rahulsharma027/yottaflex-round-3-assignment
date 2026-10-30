import json
import secrets
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from integrity.dataset import generate, TABLES, SEED, GENERATOR_VERSION
from integrity.models import Learner, Profile, Reviewer, SeedState, Submission

ACCOUNTS = [
    ("academic-admin", "academic_admin", None), ("reviewer", "instructor", "REV-001"),
    ("second-reviewer", "instructor", "REV-002"), ("appeal-reviewer", "instructor", "REV-003"),
    ("reviewer-theo", "instructor", "REV-004"), ("reviewer-anika", "instructor", "REV-005"),
    ("reviewer-evan", "instructor", "REV-006"),
    ("learner", "learner", "LRN-00001"), ("support", "support", None),
    ("platform-admin", "platform_admin", None),
]

class Command(BaseCommand):
    help = "Install a deterministic demo once. Existing data is never silently replaced."
    def add_arguments(self, parser):
        parser.add_argument("--mode", choices=["full", "starter"], default="full")

    def handle(self, *args, **options):
        state = SeedState.objects.filter(key__startswith="demo-v").first()
        if state:
            self.stdout.write(f"Preserving existing {state.mode} dataset and reviewer changes.")
            if state.key != f"demo-v{GENERATOR_VERSION}":
                self.stdout.write(self.style.WARNING(
                    f"This workspace uses an earlier dataset. Fresh workspaces use generator v{GENERATOR_VERSION}. "
                    "Choose a new YOTTA_LOCAL_DIR to inspect the refreshed dataset without replacing your existing cases."
                ))
            return
        if Submission.objects.exists():
            raise CommandError("Database has unmarked data. Refusing to seed over it; use a new YOTTA_LOCAL_DIR.")
        credentials_path = settings.LOCAL_DIR / "demo-accounts.json"
        # Write credentials first: an interrupted DB transaction can safely retry with these passwords.
        credentials = json.loads(credentials_path.read_text(encoding="utf-8")) if credentials_path.exists() else {
            username: secrets.token_urlsafe(15) for username, _, _ in ACCOUNTS
        }
        if not credentials_path.exists():
            with credentials_path.open("x", encoding="utf-8") as stream:
                json.dump(credentials, stream, indent=2)
        data, _ = generate(options["mode"], SEED)
        with transaction.atomic():
            for table in TABLES:
                model = apps.get_model("integrity", table)
                fields = {field.attname: field for field in model._meta.concrete_fields}
                objects = [model(**{name: fields[name].to_python(value) for name, value in row.items()}) for row in data[table]]
                model.objects.bulk_create(objects, batch_size=400)
            for username, role, record_id in ACCOUNTS:
                user = User.objects.create_user(username=username, password=credentials[username], first_name=username.replace("-", " ").title())
                Profile.objects.create(user=user, role=role)
                if record_id:
                    model = Learner if role == "learner" else Reviewer
                    model.objects.filter(pk=record_id).update(user=user)
            SeedState.objects.create(key=f"demo-v{GENERATOR_VERSION}", mode=options["mode"], seed=SEED)
        self.stdout.write(self.style.SUCCESS(f"Installed generator v{GENERATOR_VERSION} {options['mode']} dataset: {len(data['submission'])} submissions, {sum(r['flagged'] for r in data['similarityreport'])} flags, {len(data['case'])} cases."))
