# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
- Baseline test command / working directory / observed result / evidence: [complete]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [Booking D1 twice at 9:00 on 1 Oct 2026 is accepted. No error.]
- Expected behaviour and requirement: [: The second booking should be rejected with ValueError (FR-05, AC-04.1). A different practitioner at that time should be allowed (AC-04.2).]
- Minimal synthetic reproduction steps: [gister P1, P2, D1 and D2. Book A1 (P1, D1, 9:00). Book A2 (P2, D1, 9:00).]
- Meaningful failing test path/name and exact relevant failure: [tests/test_regressions.py::test_f8_01_same_practitioner_same_time_rejected_without_change, which fails with “DID NOT RAISE ValueError”.]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [After cancelling A1, store.find_appointment('A1') returns None.]
- Expected behaviour and requirement: [A cancelled appointment stays stored and findable, with CANCELLED status (FR-07, FR-08, AC-05.2).]
- Minimal synthetic reproduction steps: [Register P1 and D1. Book A1. Cancel A1. Look up A1.]
- Meaningful failing test path/name and exact relevant failure: [tests/test_regressions.py::test_f8_01_same_practitioner_same_time_rejected_without_change, which fails with “DID NOT RAISE ValueError”.]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [The practitioner ID check in `has_practitioner_conflict` is likely inverted (`!=` instead of `==`), so the method looks for other practitioners' bookings instead of the same practitioner's]
Evidence intended to inspect / competing explanation / discriminating check: [Evidence intended to inspect / competing explanation / discriminating check: I will inspect the comparison in `has_practitioner_conflict`, the arguments `book_appointment` passes to it, and the F8-01 test result, which fails because the second D1 booking is accepted. A competing explanation is that the store method is correct and the service layer passes the wrong ID or skips the check. To tell these apart, book D1 at 09:00 and call `has_practitioner_conflict` directly. If it returns False for D1 and True for D2, the fault is in the store method. If it returns the correct results, the fault is in the service.]
Member and saved sequence/time or commit showing this preceded consultation: [u3329873, commit ba0b30cd4ef16eadffeecd5b61e6b257b1d0fab2 ]

### F8-02 human entry
Likely cause and why plausible: [`find_appointment` likely filters out cancelled appointments with the condition `status.value != "cancelled"`, so lookup returns `None` even though the appointment is still stored. This is plausible because a cancelled appointment would then seem to disappear, even though nothing removed it from the store.]
Evidence intended to inspect / competing explanation / discriminating check: [I will inspect the loop condition in `find_appointment`, how `cancel_appointment` changes the stored appointment, and the F8-02 test result, which fails because `find_appointment('A1')` returns `None` after cancelling. A competing explanation is that `cancel_appointment` deletes or replaces the appointment instead of only changing its status. To tell these apart, cancel A1 and check `list_appointments()`. If the same object is still listed with CANCELLED status, the fault is the lookup filter. If it is missing or replaced, the fault is in `cancel_appointment`.]
Member and saved sequence/time or commit showing this preceded consultation: [u3329873 commit b9ee9441a5c424fe9c7cabac666e49c60ada99ef ]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [prompt: Observed behaviour: Booking A2 for practitioner D1 at 2026-10-01 09:00 succeeds even though A1 is already SCHEDULED for D1 at that time. Booking a different practitioner (D2) at that time is wrongly rejected.
Expected behaviour: FR-05/AC-04.1 reject the same practitioner at the same time; AC-04.2 allow a different practitioner.
Steps to reproduce: register P1, P2, D1, D2; book A1 (P1, D1, 09:00); book A2 (P2, D1, 09:00).
Failing test: tests/test_regressions.py::test_f8_01_same_practitioner_same_time_rejected_without_change - "DID NOT RAISE ValueError"
Task: Rank the three most likely causes. For each, identify the evidence I should inspect to distinguish it from the other possible causes. Do not rewrite the entire application. Do not invent requirements. Treat all suggested explanations as hypotheses.
output:Practitioner comparison is inverted (strongest; directly supported by the code). In has_practitioner_conflict, the condition tests whether the stored appointment’s practitioner ID is != practitioner_id. That skips D1’s existing booking when checking another D1 booking, but treats D1’s booking as a conflict when checking D2, matching both observations. Inspect that comparison, then check test_same_practitioner_same_time_conflict_is_rejected and test_different_practitioner_same_time_is_allowed in test_services.py.

The service passes the wrong conflict-check arguments or mishandles the result (possible, but the inspected code argues against it). Inspect the call in services.py: confirm it passes the requested practitioner ID and time, and that a True result raises ValueError. A breakpoint or spy on has_practitioner_conflict during the two bookings would distinguish this from a faulty predicate: capture its arguments and return value for D1 and D2.

The runtime data or loaded module differs from what the report assumes (lower likelihood). Inspect list_appointments() after A1 is booked: its practitioner ID, exact datetime, and status should be D1, 09:00, and SCHEDULED. Also confirm the test is importing the edited workspace’s smartcare.data_store. This would distinguish a state/import mismatch from a logic defect; the current source already shows checks for exact time and SCHEDULED status.

The first hypothesis is the best fit: the current predicate explains both the accepted D1 duplicate and rejected D2 booking. These are ranked hypotheses, not a request to change code.]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [promt: Observed behaviour: After booking and cancelling A1, store.find_appointment('A1') returns None and the service find_appointment raises LookupError. A1 is still in store.list_appointments().
Expected behaviour: FR-07/FR-08/AC-05.2 — a cancelled appointment is retained and findable as the same object with CANCELLED status.
Steps to reproduce: register P1, D1; book A1 (P1, D1, 2026-10-01 09:00); cancel A1; call store.find_appointment('A1').
Failing test: tests/test_regressions.py::test_f8_02_cancelled_appointment_is_retained_and_found - "assert None is <Appointment>"
Task: Rank the three most likely causes. For each, identify the evidence I should inspect to distinguish it from the other possible causes. Do not rewrite the entire application. Do not invent requirements. Treat all suggested explanations as hypotheses.

output: The store lookup excludes cancelled appointments (strongest). In data_store.py, find_appointment returns a matching ID only when appointment.status.value != "cancelled". That condition filters out A1 precisely when its status is CANCELLED. Inspect the stored A1 after cancellation: if it is the original object and its status is CANCELLED, this confirms the lookup filter as the cause. The existing retained-history assertions in test_services.py also specify that cancelled appointments remain findable.

Cancellation leaves A1 in an unexpected state or replaces it (weaker). The list may contain an appointment under A1, but that alone does not establish it is the original object with CANCELLED status. Compare the listed object with the object returned by booking (is), and inspect its ID and status after cancellation. If it is the original object with CANCELLED status, this hypothesis is ruled out. The current domain cancellation method changes status without deleting the appointment.

Lookup uses a different ID, store instance, or loaded implementation (least likely). Compare the queried ID with the stored appointment ID, check that the store used for list_appointments() is the same one used for find_appointment(), and confirm the test imports this project’s smartcare.data_store. These checks distinguish a lookup-context mismatch from the status filter. Because the store-level lookup itself returns None, the service’s LookupError is likely a consequence, not the primary cause: services.py raises it when the store returns None. These remain hypotheses until the object’s post-cancellation identity/status and lookup path are checked.]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [c5200cf] | [python -m pytest -q tests/test_regressions.py] | [FAILED tests/test_regressions.py::test_f8_01_same_practitioner_same_time_rejected_without_change - Failed: DID NOT RAISE ValueError] |
| F8-01 after repair | [1ad49a2] | [python -m pytest -q tests/test_regressions.py] | [FAILED tests/test_regressions.py::test_f8_02_cancelled_appointment_is_retained_and_found - AssertionError: assert None is <smartcare.domain.Appointment object at 0x00000227C6190BC0>
1 failed, 1 passed in 0.19s] |
| F8-02 before repair | [c5200cf] | [python -m pytest -q tests/test_regressions.py] | [FAILED tests/test_regressions.py::test_f8_02_cancelled_appointment_is_retained_and_found - AssertionError: assert None is <smartcare.domain.Appointment object at 0x000001D8F7C951F0>] |
| F8-02 after repair | [9084282] | [python -m pytest -q tests/test_regressions.py] | [2 passed in 0.02s] |
| Full suite after both repairs, before refactor | [9084282] | [python -m pytest -q] | [76 passed in 0.13s] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [F8-01: `pytest.raises(ValueError)` catches the faulty code accepting a second D1 booking at 09:00. The test also checks nothing was stored by the rejected booking, and that D2 at 09:00 is still allowed (AC-04.2).
F8-02: `assert store.find_appointment('A1') is booked` catches the faulty code returning None after cancellation. The test also checks the status is CANCELLED, the appointment is still listed and findable through the service (FR-07/AC-05.2), and a second cancel is rejected without changes (BR-07).]
Unrelated failures investigated / resolution: [None. All 7 initial failures were caused by the two defects: 4 conflict tests passed after the F8-01 repair, and the 3 cancellation tests passed after the F8-02 repair. Full suite after both: 76 passed.]

## H. Refactoring decision and before/after verification

Smell and exact location: [Magic string `"scheduled"` in `has_practitioner_conflict`, `project/smartcare/data_store.py` line 112 (`appointment.status.value == "scheduled"`).]
Small proposed structural change / why justified: [Replace it with the existing enum, `appointment.status is AppointmentStatus.SCHEDULED`. This matches the rest of the code, avoids typos in a raw string, and stays correct if the enum's text value ever changes.]
External behaviour to preserve / relevant tests: [ A same-practitioner SCHEDULED booking is still a conflict, a different practitioner is still allowed, a cancelled booking does not block the slot, and the check changes nothing. Covered by `tests/test_regressions.py` and the conflict tests in `tests/test_services.py`]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
