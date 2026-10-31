# YottaFlex AI: 72 Hours Code Challenge

## Confirmed context

- Candidate identity and private correspondence are excluded from this public preparation note.
- Round: 3, following the AI Screening.
- Candidate-reported start: October 30, 2026 at 03:16 IST.
- **Invitation deadline: Monday, November 2, 2026 at 03:03:19 IST.**
- Use the invitation deadline as the working cutoff. It is 12 minutes 41 seconds earlier than 72 hours after the candidate-reported start.
- AI coding tools are permitted. The candidate must understand and be able to explain the submitted code.
- Problem statement portal: [REDACTED: candidate-specific private application URL].
- The initial portal access problem was reported resolved by Rahul on October 30, 2026. The supplied statement and both supporting PDFs have now been reviewed.

## Problem statement received

- Domain: academic-integrity case management, from synthetic similarity flags through evidence, reviewer assignment, decisions, appeals, and closure.
- Full dataset: 10,000 submissions, 1,000 flags, and 300 cases, with labelled negative scenarios, separate ground truth, validation, and two-run reproducibility proof.
- Detailed beginner explanation, requirements, proposed architecture, and source interpretation: `PROJECT_BREAKDOWN.md`.
- Reusable planning/implementation handoff prompt with guardrails: `LLM_PROJECT_PROMPT.md`.
- Implementation has started in this repository. README.md, REQUIREMENTS.md, DEVELOPMENT.md, and VERIFICATION.md describe current behavior and evidence; planning notes below retain their historical context.
- User priorities: polished, user-friendly screens and easy local setup after cloning. See README.md for the implemented launcher and REVIEWER_EXPERIENCE.md for the original acceptance criteria.
- Any deadline clarification from support remains pending. Until then, retain the invitation cutoff above.

## Skill package setup

- Requested package: <https://github.com/alirezarezvani/claude-skills>.
- Installed globally with `npx --yes codex-marketplace add alirezarezvani/claude-skills --plugin --global`.
- Installed plugin: `claude-code-skills`, version `2.14.3`, source revision `0496583603e56cdd5022dd61c823bd784a80a752`.
- Windows checked out the Codex skill links as text files. The installed copy was repaired by preserving those pointer files and copying their verified skill directories into the plugin's `.codex/skills` directory. A reinstall or update may need the same verification.
- Keep the installed package outside the submission repository; apply relevant skills according to the work being done.

## Submission requirements from the invitation

- Put the code and everything required by the problem statement into one GitHub repository.
- The repository must be public.
- Submit the repository link on the portal before the deadline.
- Verify the public repository link in a private browser window before submitting.

## Additional requirements from the supplied PDFs

- Include every prompt submitted to every AI tool used; responses are optional. Disclose export limitations and visible privacy redactions.
- Explain AI reliance and actual candidate review, changes, and validation without inventing personal review actions.
- Include clear installation/configuration/run/verification instructions and reasoning, assumptions, tradeoffs, and limitations.
- Show meaningful development history. The challenge window is based on the recorded project-send timestamp, and artifact timestamps are checked.
- Keep the work individual; AI tools and public resources are allowed, implementation help from other people is not.
- Use free or locally runnable services and avoid unnecessarily large/slow dependencies.
- A hosted demo and a formal automated test suite are optional under the FAQ; project-specific data validation and repeatability proof remain required.
- Do not reuse an existing complete/core solution or publish secrets, sensitive information, or unauthorized code.
- Keep the dedicated public repository available/editable through the deadline. The FAQ also mentions email submission; the specific invitation asks for portal submission. Follow later official clarification if provided.

## Execution sequence after the statement arrives

1. Extract every explicit requirement and create a traceable implementation checklist.
2. Choose the smallest suitable architecture and document its tradeoffs.
3. Build a working end-to-end flow covering the core requirement.
4. Complete remaining required behavior and meaningful tests.
5. Verify interface behavior, error cases, and responsive layouts where applicable.
6. Finish setup instructions, required deliverables, and a final requirement review.
7. Verify public access and submit with time remaining before the cutoff.

## Final checklist

- [ ] Every problem statement requirement is implemented or an explicit limitation is documented.
- [ ] Required deliverables are present in the repository.
- [ ] Setup and run instructions work from a fresh checkout.
- [ ] Appropriate checks pass and their results are recorded.
- [ ] Prompt history across AI tools and honest AI-use disclosure are included, with any limitations stated.
- [ ] Full data volumes, required scenarios, separate ground truth, validation, exports, and two-run checksums are present.
- [ ] No secrets or private candidate correspondence are included in the public submission.
- [ ] Rahul can explain the implementation and key decisions.
- [ ] GitHub repository is public and accessible in a private browser window.
- [ ] Repository URL is submitted through the portal before the deadline.

The initial implementation session used the recorded source interpretation. On 2026-10-31 the original pasted statement and both PDFs were recovered into [docs/source](source/README.md); the agent reread them for the disclosure/reasoning documentation. Final candidate source-to-implementation reconciliation remains necessary. The checklist above is a submission checklist, not a claim that every external action is complete.
