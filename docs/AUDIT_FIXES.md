# Prioritized audit fixes

Audit baseline: `67a8ad0`, 2026-10-30. Findings are addressed separately, with verification and a commit before moving to the next item. The initial 31-test suite passed despite the reproduced gaps; passing it alone was insufficient.

For setup, role switches and expected pass/fail observations, use the [manual reviewer walkthrough](WALKTHROUGH.md#completed-audit-fixes-manual-checks). F4–F6 are deferred; this documentation update does not implement additional fixes.

| Finding | Status | Required follow-up |
|---|---|---|
| F1: learner-response dead end for unlinked learners | Fixed and verified | Staff capture of received correspondence now preserves source, recorder and response history |
| F2: learner supersession of staff evidence | Fixed and verified | Shared replacement policy protects staff evidence and permits learner-owned revisions/separate rebuttals |
| F3: future appeal information / perfect assessment-label correlation | Fixed and verified | Generator revision 2 separates academic text from process facts and mixes scenario/assessment assignments; archive/proof regenerated |
| F4: late learner response accepted by validator | Open | Validate response-event chronology against decisions |
| F5: mobile table semantics and secondary text contrast | Open | Restore accessible relationships and correct low-contrast text |
| F6: prompt-history and personal-review reconciliation | Open | Reconcile available records and document actual candidate validation honestly |

## F1 — response reachability

User chose to retain the ten demo accounts and let administrators/support record responses received outside the portal. A dedicated service/form requires a substantive response, source reference, prior notice and an open review/appeal. The route is limited to learners without linked portal accounts; direct learner responses retain their existing ownership rules.

The case stores the latest response. A `learner_response_recorded` event retains each full response/source snapshot, the real staff actor, recorded time and learner ID. Case files display that external provenance clearly. Staff responses remain staff-recorded actions; no learner impersonation, automatic response, account creation or decision bypass is introduced. Existing unanswered cases can proceed when a response is deliberately supplied.

Verification: five additional regression tests plus existing checks, 36 tests total, passed on Python 3.14.10. Coverage includes an unlinked learner's full review/decision/closure, allowed/forbidden roles, refusal for linked learners, notice/state/source constraints, rollback/stale protection, retained history, escaped output and form validation. Browser verification used a separate workspace at desktop and phone sizes. No migration or generated dataset change is required. See VERIFICATION.md for the measured results. Later findings remain open.

## F2 — evidence replacement authority

The original audit exploit now has a regression test: attempting to supersede staff evidence from a learner account is rejected, with case version, evidence count, decision choices and timeline unchanged. Learners may add rebuttals to their own cases and revise only their own current evidence. Staff retain their existing correction authority. A shared query policy supplies both form choices and the service-level authorization check, so forged POSTs and direct service calls cannot bypass the restriction.

Five new tests cover direct and forged replacement attempts, ignored client authorship, separate rebuttals and authorized own revisions, actor/case-specific choices, stale/branched/cross-case requests, retained history and evidence-backed decisions. The earlier late-evidence history test now uses an authorized staff correction. All 41 tests pass on Python 3.14.10. Desktop/phone browser checks used a separate workspace. No migration, export regeneration or live-case edit was needed. F3–F6 remain open.

## F3 — temporal content and metadata shortcuts

Two regressions first reproduced future appeal text and assessment/scenario coupling. Revision 2 now writes academic passages into Submission.content, retaining source observations and later attribution evidence in dated records. Scenarios are shuffled within score strata with reserved walkthroughs; assessment assignments use a separate seeded shuffled plan. All five families occur under every assessment, and 1,342 learners have both outcome labels in the default full dataset.

Regenerated `data/full-dataset.zip`, `verification.json` and `python314-verification.json`. Every archive entry matches its recorded hash. Python 3.12/3.14 independently reproduced matching counts and per-file hashes, zero baseline findings and all four designed detections. All 46 tests pass, including temporal-content, distribution, walkthrough-boundary and seed-preservation checks. A fresh full browser workspace is marked `demo-v2`. Legacy workspaces warn and preserve data/passwords; README gives a separate-workspace command. No migration or automatic overwrite is needed. F4–F6 remain open; these checks do not establish general absence of dataset bias or real plagiarism-detection accuracy.
