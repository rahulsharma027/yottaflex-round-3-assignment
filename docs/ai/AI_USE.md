# AI assistance and candidate review

Updated 2026-10-31 (Asia/Kolkata). AI reliance was **heavy**, including core implementation. Rahul directed the work and reviewed it; Codex authored substantial code and documentation and executed the recorded automated/browser checks. The application itself does not call an LLM.

## Where AI accelerated the work

| Area | AI contribution | Reliance and limits |
|---|---|---|
| Understanding and planning | Interpreted the statement, broke down deliverables, proposed the schema, lifecycle, milestones and stack alternatives | Heavy assistance; the supplied sources are now preserved in [source](../source/README.md) for comparison |
| Backend and local setup | Authored Django models/migrations, forms/views, transactional services, role checks, management commands and the launcher | Heavy core-code reliance; framework auth, ORM and migration behavior come from pinned dependencies |
| Synthetic data and evaluation | Authored generation, CSV/JSON/SQL exports, separate truth, four invalid fixtures, validation and repeatability tooling | Heavy reliance; synthetic results demonstrate the designed checks, not real plagiarism-detection accuracy |
| Interface and iteration | Implemented templates, CSS, progressive JavaScript, login help, queue navigation, case layout and palette changes | AI implemented the code; Rahul supplied usability findings, priorities and design choices |
| Debugging and review | Investigated reported bugs, conducted architecture/code/interface audits, reproduced F1–F3 and implemented regressions/fixes | Agent self-review and agent-authored tests share possible blind spots; open findings remain explicit |
| Verification and explanation | Ran commands/browser checks, generated proof/screenshots, drafted architecture, reasoning and reviewer documentation | Execution results are attributed to the agent; Rahul's personal activities are recorded separately below |

The core project was newly authored for this assessment with AI assistance. No complete existing core solution was imported. Standard dependencies are pinned in [requirements.txt](../../requirements.txt); development skills supplied guidance rather than a second runtime. The available project record reports no implementation subagents or image-generation use.

## What Rahul personally reviewed, changed or validated

See [CANDIDATE_REVIEW.md](CANDIDATE_REVIEW.md) for the evidence and attribution of each contribution. The conversation records Rahul exploring the interface across actors, identifying missing login guidance and queue behavior, reporting the broken All cases switch, choosing reviewer-only assignment controls and the case-file order, directing the navy/blue theme and naming, and selecting sourced external responses while retaining ten demo accounts. Codex implemented those requested code changes.

On 2026-10-31 Rahul additionally confirmed reviewing the whole codebase, including `integrity`, scripts, static assets, templates, management commands, migrations and generated documentation, alongside the AI and architecture audits. This is a candidate-reported review. It does not establish that Rahul personally executed the automated tests, export commands or every manual workflow, nor is it an independent assessment of his understanding.

The latest recorded **46-test** run and Python 3.12/3.14 export checks were executed by the agent. Actual results, environments and limitations are in [VERIFICATION.md](../VERIFICATION.md); the reader-facing explanation is [REASONING.md](../REASONING.md). No human code edits or separate candidate test execution are claimed without evidence.

## Prompt record, tools and coverage

Rahul answered **“Only this Codex chat”** when asked about other AI tools/chats on 2026-10-31. The app also retains the earlier project preparation chat. Both project chats were recovered and are named in [PROMPTS.json](PROMPTS.json). No separate external AI tool use is reported; use of the drafted [handoff prompt](../LLM_PROJECT_PROMPT.md) in another tool is not established.

- [PROMPTS.json](PROMPTS.json) contains the candidate-input messages exposed by the app for those two project chats, with turn/message identifiers and turn-start timestamps. Pagination was exhausted for each chat. Privacy redactions and omitted automatic browser context are explicitly marked.
- [PROMPT_HISTORY.md](PROMPT_HISTORY.md) is the readable narrative of requests, decisions, AI assistance and coverage limitations. It is not an unredacted session export.
- [IMPLEMENTATION_TOOL_LOG.md](IMPLEMENTATION_TOOL_LOG.md) summarizes research, development tooling and checks. It is not an exact export of every tool payload.
- [Source attachments](../source/README.md) preserve the pasted problem statement and both PDFs. The current [AGENTS.md](../../AGENTS.md) is retained; every earlier version of automatically supplied instructions/context is not reproduced in this record.

AI replies are omitted as allowed by FAQ question 6. Internal reasoning, complete tool outputs, system/model instructions and full historical environment context are not published. The recovered user-message record materially improves coverage, but it is not a claim of a complete raw session export or independent proof that no undisclosed tools were used. The active turn can receive further messages after a snapshot; the export must be refreshed when new project prompts arrive. These limits remain disclosed rather than marking F6 closed.

## Privacy and remaining scope

Private recruitment correspondence, candidate-specific application links, personal local paths, credentials, secrets and tooling caches are excluded or visibly redacted. The public sources contain the assignment/guidance, not private recruitment email. Never commit `.local` or `.venv`.

This update documents transparency and reasoning. F4–F6 remain open/deferred in [AUDIT_FIXES.md](../AUDIT_FIXES.md); no validator or accessibility fix, complete disclosure certification, portal submission or independent candidate assessment is claimed.
