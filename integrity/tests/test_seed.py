import io
import tempfile
from pathlib import Path
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, override_settings
from integrity.dataset import GENERATOR_VERSION
from integrity.models import Case, SeedState, Submission


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class SeedVersionTests(TestCase):
    def test_fresh_seed_is_versioned_and_repeat_run_preserves_data_and_passwords(self):
        with tempfile.TemporaryDirectory() as directory, override_settings(LOCAL_DIR=Path(directory)):
            call_command("seed_demo", mode="starter", stdout=io.StringIO())
            self.assertEqual(SeedState.objects.get().key, f"demo-v{GENERATOR_VERSION}")
            self.assertEqual((Submission.objects.count(), Case.objects.count(), User.objects.count()), (100, 3, 10))
            credentials = (Path(directory) / "demo-accounts.json").read_bytes()
            Submission.objects.filter(pk="SUB-2026-000001").update(title="Preserve this reviewer edit")
            output = io.StringIO()
            call_command("seed_demo", mode="full", stdout=output)
            self.assertIn("Preserving existing starter dataset", output.getvalue())
            self.assertEqual(Submission.objects.get(pk="SUB-2026-000001").title, "Preserve this reviewer edit")
            self.assertEqual(Submission.objects.count(), 100)
            self.assertEqual((Path(directory) / "demo-accounts.json").read_bytes(), credentials)

    def test_legacy_seed_warns_without_replacing_cases_or_credentials(self):
        with tempfile.TemporaryDirectory() as directory, override_settings(LOCAL_DIR=Path(directory)):
            call_command("seed_demo", mode="starter", stdout=io.StringIO())
            SeedState.objects.update(key="demo-v1")
            Case.objects.filter(pk="INT-2026-000001").update(version=9)
            credentials = (Path(directory) / "demo-accounts.json").read_bytes()
            output = io.StringIO()
            call_command("seed_demo", mode="full", stdout=output)
            self.assertIn("earlier dataset", output.getvalue())
            self.assertIn("new YOTTA_LOCAL_DIR", output.getvalue())
            self.assertEqual(SeedState.objects.get().key, "demo-v1")
            self.assertEqual(Case.objects.get(pk="INT-2026-000001").version, 9)
            self.assertEqual((Submission.objects.count(), User.objects.count()), (100, 10))
            self.assertEqual((Path(directory) / "demo-accounts.json").read_bytes(), credentials)
