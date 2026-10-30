# YottaFlex AI code challenge

## Objective and deadline

- Build the supplied problem statement once it becomes available. Do not invent requirements or select the application stack before reviewing it.
- Submission cutoff from the invitation: **2026-11-02 03:03:19 Asia/Kolkata** (2026-11-01 21:33:19 UTC).
- See `docs/CHALLENGE.md` for confirmed requirements, pending information, and the submission checklist.

## Working approach

- Apply the available skills that are relevant to each task, including the installed `alirezarezvani/claude-skills` package. Read each selected skill before using it.
- The requested package is installed globally as `claude-code-skills` under the agent's Codex plugin directory. Its Codex skill instructions are under `.codex/skills/<skill-name>/SKILL.md`; use these local instructions if the package is not yet listed in the current session's skill catalog. Agent tooling is not a reviewer prerequisite. [REDACTED: personal local installation path.]
- For interface work, use the applicable frontend design, responsive layout, and interface polish skills. Choose a coherent direction and verify it in a browser at desktop and mobile sizes.
- User priorities: a polished, friendly case-management interface and minimal local setup for a reviewer cloning the repository. Follow `docs/REVIEWER_EXPERIENCE.md`; aim for one documented launcher command that prepares local configuration, migrations, demo users, and synthetic data, then starts the app. Keep subsequent runs non-destructive and avoid required cloud services or external database setup.
- Select architecture, backend, testing, and security skills according to the actual problem statement and chosen stack.
- Keep the implementation focused on the assessment requirements and the time available. Prioritize a working end-to-end flow, then validation, documentation, and polish.
- Run checks appropriate to each change. Record real verification results and clearly identify any remaining limitations.
- Keep the code understandable and document meaningful decisions so Rahul can explain the implementation in a later interview.
- Keep secrets and local tooling caches out of the public repository.
- Keep source code and all deliverables required by the problem statement together in one repository.

## Completion

- Confirm the repository is public and accessible while signed out.
- Verify that a fresh checkout can follow the documented setup and run instructions.
- Check every requirement against the final implementation and provide the repository link for submission before the cutoff.
