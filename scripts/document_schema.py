"""Generate the field dictionary from the actual migrated Django model metadata."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.apps import apps
from django.db.models import NOT_PROVIDED

def main():
    text = ["# Schema and data dictionary", "", "Generated from `integrity/models.py` by `python scripts/document_schema.py`. Check migrations into Git with model changes.", "",
        "All core and supporting application fields are listed below. SQL export tables use the lowercase model name and `_id` foreign-key columns. CSV uses empty cells for nulls; JSON uses null. SQL represents booleans as 0/1. Live user links are omitted from deterministic exports and attached only during local account creation.", "",
        "IDs are immutable text primary keys unless a table explicitly uses an automatic integer. Deletion of referenced records is protected. No delete or in-place evidence/decision edit route is exposed. Char fields use Unicode; datetime values are timezone-aware ISO 8601 (UTC in exports, Asia/Kolkata in the interface). Scores and thresholds use percentage points on 0–100; case version is a positive optimistic-lock counter. Dates and historical IDs are fixed by the generator, while new actions use the current clock.", "",
        "`Required` refers to database nullability; a blank text field stores an empty string when allowed. Django form requirements may be stricter. Constraints, lifecycle, cardinalities, and cross-table checks are documented in ARCHITECTURE.md and DATASET.md. Django's auth/session tables use the framework's standard migrations; passwords are hashed by Django and excluded from every export.", ""]
    for model in apps.get_app_config("integrity").get_models():
        text += [f"## {model.__name__}", "", "| Field | Type | Required | Unique | Values / validation / relationship |", "|---|---|---|---|---|"]
        for field in model._meta.concrete_fields:
            details = []
            if field.primary_key:
                details.append("Primary key")
            if field.max_length:
                details.append(f"Max {field.max_length} characters")
            if field.choices:
                details.append("Allowed: " + ", ".join(f"`{value}`" for value, _ in field.choices))
            if field.is_relation:
                details.append(f"FK → {field.related_model.__name__}.id; protected delete; " + ("1:1" if field.one_to_one else "N:1"))
            if field.blank:
                details.append("Blank allowed")
            if field.default is not NOT_PROVIDED:
                details.append("Default: " + (getattr(field.default, "__name__", str(field.default)) if callable(field.default) else str(field.default)))
            for validator in field.validators:
                if hasattr(validator, "limit_value"):
                    details.append(f"{type(validator).__name__}: {validator.limit_value}")
            if field.name in {"email"}:
                details.append("Valid email format; synthetic .invalid domain")
            text.append(f"| `{field.attname}` | {field.get_internal_type()} | {'No' if field.null else 'Yes'} | {'Yes' if field.unique else 'No'} | {'; '.join(details)} |")
        for constraint in model._meta.constraints:
            text += ["", f"Constraint `{constraint.name}`: `{constraint}`"]
        text.append("")
    (ROOT / "docs" / "SCHEMA.md").write_text("\n".join(text), encoding="utf-8", newline="\n")
    print("Updated docs/SCHEMA.md from model metadata.")

if __name__ == "__main__":
    main()
