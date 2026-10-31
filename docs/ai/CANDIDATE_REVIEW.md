# Candidate contribution and personal review

Recorded on 2026-10-31 (Asia/Kolkata). This record distinguishes candidate statements and feedback from checks executed by Codex. Supporting prompts are in [PROMPTS.json](PROMPTS.json) and the readable [prompt history](PROMPT_HISTORY.md). It is not a checklist of activities assumed to have occurred.

## Review and decisions evidenced by the conversation

| Candidate activity | Evidence in the project conversation | Result and attribution |
|---|---|---|
| Set the delivery priorities | Requested component-by-component implementation, documentation inside `/Yotta`, a clean repository and easy reviewer setup | Rahul set priorities; Codex proposed and implemented the technical approach |
| Reviewed the first-run experience | Reported that the portal opened at login and that username/password guidance was confusing | Rahul identified the usability problem; Codex added the in-page guide |
| Explored role interfaces | Said he was going through the interface as all actors; identified static summary cards and missing reviewer assignment defaults | Candidate-reported interface exploration; this does not prove completion of every role's workflow |
| Reported and checked assignment navigation | Reported Assigned to me working by default but All cases failing; subsequently requested removal of irrelevant assignment controls and said the result looked good | Rahul supplied bug feedback and acceptance; Codex corrected the implementation and ran regressions/browser checks |
| Chose the case-file information order | Accepted learner details/submitted work first, then evidence, decisions and timeline with actions alongside | Rahul selected the proposed order; Codex implemented the structured file, including Response |
| Directed naming and presentation | Requested ACI (Academic Integrity) Portal By Yotta, a navy/blue sidebar and lighter central content; said the result looked good | Candidate product/design direction, implemented by Codex |
| Selected the unlinked-learner response workflow | Chose to retain ten demo accounts and let administrators/support record sourced external responses | Candidate workflow choice; Codex implemented F1 with staff attribution and prerequisites |
| Directed review and prioritization | Requested a harsh senior-reviewer audit, then separate prioritized fixes/commits; later deferred further findings | Rahul set review scope and priorities; audits and technical reproduction were performed by the agent |

These entries describe decisions, reported observations and feedback. They do not attribute agent-authored code to the candidate.

## Candidate-confirmed code and documentation review

In response to a direct question about personal review on 2026-10-31, Rahul stated:

> Apart from the interface, I have gone through the whole code base, integrity, scripts, static templates, all these things, and managements, migrations, and all the documentation that we generated, alongside with all the AI and architecture audits we have conducted throughout the project. Yeah, that's it.

Recorded scope: the codebase, `integrity`, scripts, static assets, templates, management commands, migrations, generated documentation and the AI/architecture audit findings. This is Rahul's account of his review. It is not an independent line-by-line verification, a demonstration of complete technical understanding, or evidence of additional tests being run.

## Verification ownership and unclaimed activities

| Activity | Recorded executor/status |
|---|---|
| Interface exploration, usability feedback and requested product/workflow changes | Rahul, as reported in the conversation |
| Code/documentation/audit review described above | Rahul, confirmed on 2026-10-31 |
| Latest automated suite: 46 passing tests on Python 3.14 | Codex; historical execution details in [VERIFICATION.md](../VERIFICATION.md) |
| Python 3.12/3.14 export comparison, hashes, archive checks and designed exception detection | Codex; packaged reports under `data/` |
| Recorded desktop/phone/tablet screenshots and browser verification | Codex; bounded surfaces and results in VERIFICATION.md |
| Candidate personally executing automated tests or export verification | Not reported; no claim made |
| Candidate personally completing every lifecycle/appeal/negative-fixture check | Not established by the available statements |
| Candidate manually editing source code | No specific manual code edit reported; requested changes were implemented by Codex |

Additional review can be recorded when it actually occurs, with the relevant file/workflow, what was checked, the observed outcome and any resulting change. The [manual walkthrough](../WALKTHROUGH.md) provides reproducible steps for that purpose; its existence is not evidence that the candidate has completed it.
