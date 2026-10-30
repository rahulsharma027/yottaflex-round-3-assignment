# Prioritized audit fixes

Audit baseline: `67a8ad0`, 2026-10-30. Findings are addressed separately, with verification and a commit before moving to the next item. The initial 31-test suite passed despite the reproduced gaps; passing it alone was insufficient.

| Finding | Status | Required follow-up |
|---|---|---|
| F1: learner-response dead end for unlinked learners | Fixed and verified | Staff capture of received correspondence now preserves source, recorder and response history |
| F2: learner supersession of staff evidence | Open | Restrict replacement authority while preserving separate learner rebuttals |
| F3: future appeal information / perfect assessment-label correlation | Open | Repair generator independence and regenerate exports/proof |
| F4: late learner response accepted by validator | Open | Validate response-event chronology against decisions |
| F5: mobile table semantics and secondary text contrast | Open | Restore accessible relationships and correct low-contrast text |
| F6: prompt-history and personal-review reconciliation | Open | Reconcile available records and document actual candidate validation honestly |

## F1 — response reachability

User chose to retain the ten demo accounts and let administrators/support record responses received outside the portal. A dedicated service/form requires a substantive response, source reference, prior notice and an open review/appeal. The route is limited to learners without linked portal accounts; direct learner responses retain their existing ownership rules.

The case stores the latest response. A `learner_response_recorded` event retains each full response/source snapshot, the real staff actor, recorded time and learner ID. Case files display that external provenance clearly. Staff responses remain staff-recorded actions; no learner impersonation, automatic response, account creation or decision bypass is introduced. Existing unanswered cases can proceed when a response is deliberately supplied.

Verification: five additional regression tests plus existing checks, 36 tests total, passed on Python 3.14.10. Coverage includes an unlinked learner's full review/decision/closure, allowed/forbidden roles, refusal for linked learners, notice/state/source constraints, rollback/stale protection, retained history, escaped output and form validation. Browser verification used a separate workspace at desktop and phone sizes. No migration or generated dataset change is required. See VERIFICATION.md for the measured results. Later findings remain open.
