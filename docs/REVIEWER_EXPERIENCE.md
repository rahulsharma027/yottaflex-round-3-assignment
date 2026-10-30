# Interface and local reviewer experience

Original acceptance criteria. A launcher and interface are now implemented; README.md describes usage and VERIFICATION.md records actual checks and remaining limits. Statements below retain the original target wording.

## User priorities

Rahul wants a polished, friendly interface and straightforward local configuration for a reviewer who clones the repository. These are user requirements, in addition to the assessment requirements.

## First-run experience

Target journey: clone the repository, enter its directory, run one documented launcher command, and open the printed local URL with synthetic demo data ready.

The proposed stack remains Python + Django + SQLite + custom templates/CSS and small JavaScript enhancements. A separate React application is an option, but visual quality does not require changing the proposed architecture. Choose the final stack based on both interaction needs and setup effort.

The launcher should:

1. Check the documented supported Python version and required tools; explain any missing prerequisite and the next step.
2. Create an isolated local environment and install pinned dependencies on first use. State that initial dependency installation needs internet access.
3. Generate local-only configuration and a random development secret in ignored files.
4. Apply database migrations and seed the full synthetic demonstration dataset on first use: 10,000 submissions, 1,000 flags, and 300 cases. Include a smaller explicit quick mode if useful, labelled with its actual counts.
5. Create synthetic demo users for the named roles and generate local demo credentials, displaying them to the reviewer without committing passwords or secrets.
6. Start one application server on the loopback interface and print the URL, dataset mode, and how to stop it. Provide a clear override if the port is occupied.

Repeat launches must preserve reviewer-created cases and decisions, skip unchanged setup/seed steps, and recover clearly from interrupted initialization. Do not silently erase or reseed a database. An explicit demo reset must say what it changes and require confirmation or a deliberately supplied reset flag. Optional Docker instructions may supplement the native route.

After dependencies and local assets are installed, core operation must work without internet, paid services, cloud accounts, external databases, or CDN-hosted fonts/scripts. Do not require Node.js for reviewers if the chosen templates-based solution does not need it. Any future frontend build should be reproducible and its prerequisites made explicit.

## Interface priorities

- Give the app a coherent visual identity and calm, readable typography. Follow the app-screen design workflow when actual UI work begins; decide palette, type, and layout from the product's tasks.
- Lead with the review queue and the next useful action. Put evidence, rationale, and the case timeline at the center of case detail.
- Use explicit action labels such as "Assign reviewer", "Record decision", and "Submit appeal".
- Keep similarity warnings visually distinct from human findings. A high score must never look like an automatic misconduct verdict.
- Provide search, useful filters, sorting, pagination, result counts, and a clear way to reset filters. Preserve queue context when returning from a case.
- Give decisions and appeals clear prerequisites. Explain blocked actions, conflicts, and missing evidence; preserve entered form values on validation failures.
- Show success, empty, unavailable, loading, denied, and recoverable error states where applicable. Prevent accidental duplicate submissions.
- Support keyboard use, visible focus, readable contrast, labelled fields, and status text that does not depend on color alone.
- Adapt navigation, tables, evidence, and timelines for mobile and tablet use. Verify desktop and mobile screenshots and complete interactions in a browser.
- Keep all counts and charts derived from stored data and label the dataset as synthetic. Restrict ground truth to evaluation outputs rather than the operational review UI.

## Guided assessment walkthrough

Provide a local "Explore demo cases" entry point linking to a legitimate quotation/template case, a cleared false positive, a case with multiple reviewers, and a successful appeal. Include an authorized validation view of the four isolated negative scenarios and detected violations. These links should make the work discoverable without exposing expected labels as review inputs or weakening server-side permissions.

Clearly distinguish role accounts and permissions. Any optional quick role-entry feature must be limited to explicit local demo mode and still create an appropriate server-side session; never trust a browser-selected role as authorization.

## Verification before submission

- Follow the README from a fresh checkout in a clean location; record the exact environment, command, observed setup time, and result.
- Check initial setup, second launch, data persistence, occupied port, missing prerequisite, failed dependency install, and explicit reset behavior.
- Verify the promised platform routes; do not label an untested platform as tested.
- After setup, run the workflow with external network access unavailable and confirm assets and core features still work.
- Walk a case through review, decision, and independent appeal using the documented demo users.
- Inspect layouts at phone, tablet, and desktop widths, and check keyboard access and validation feedback.

This document is an implementation target. Do not present these checks, startup performance, or controls as completed until they have actually been verified.
