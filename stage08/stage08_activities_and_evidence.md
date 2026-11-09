# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Fri 8:30 Group 1
Members and UG/PG cohorts: [Group/tutorial: Fri 8:30 Group 1
Members and UG/PG cohorts: Aadhya Singh, Ben Parnell, Izayah Baker, Lachlan O'Meara UG]
Record owner / contribution links for each member: Record owner: Lachlan O'Meara. Lachlan O'Meara: preparation, tests, diagnosis, repairs and refactor (commits 2d4b8df–0c10c78 on debug/stage08, PRs #4 and #10, issues #7–#9). Ben Parnell: review, merge and retest of PR #10 (https://github.com/BenP64/st1-assignment-3/pull/10), merge of PR #4. 

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

Response and reason: [
- "Appointment disappears after cancellation." = **Symptom.** It describes what was observed, not why. "Disappears" is also vague: our check showed A1 was still in `list_appointments()`, it just couldn't be found by lookup.
- "The data-store removal path is probably being called." = **Hypothesis.** It is a testable explanation. Tested against our project: there is no delete method, and after cancelling, A1 was still in `list_appointments()` as the same object with CANCELLED status (copilot_check_f8_02.py). So this hypothesis was disproved.
- "The failing test shows store.find_appointment('A1') returns None." = **Evidence.** It is a concrete, observed value from a test run (test_regressions.py line 74).
- "The service layer is badly designed." =**Opinion.** It gives no specific cause and no check that could prove or disprove it, so it is not a diagnosis.
- "Traceback points to smartcare/services.py line 42 in the example." = **Evidence**,It shows where the error was raised, but not why it happened. In our run, `test_cancelled_appointment_remains_retrievable` failed with LookupError at services.py line 136, but the root cause was in data_store.py `find_appointment`, which returned None. The service only reported it.]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason:
Scenario chosen: same-practitioner/same-time booking (F8-01). Full record in sections C and E, written before any code was changed.
- Expected: a second SCHEDULED booking for the same practitioner at the same time is rejected with ValueError and nothing is stored a different practitioner at that time is allowed (FR-05, AC-04.1, AC-04.2).
- Observed: booking A2 for D1 at 2026-10-01 09:00 was accepted although A1 was already booked for D1 then. booking D2 at that time was rejected.
- Minimal reproduction: register P1, P2, D1, D2 book A1 (P1, D1, 09:00) book A2 (P2, D1, 09:00).
- Initial hypothesis: the practitioner ID comparison in `has_practitioner_conflict` is inverted (`!=` instead of `==`).
- Evidence to inspect: the comparison in `has_practitioner_conflict`, the arguments `book_appointment` passes to it and a direct call to the store method for D1 and D2 to separate a store fault from a service fault.
Reason: the requirement defines the expected result, so the test checks the contract rather than whatever the code currently does. Recording the hypothesis before changing code keeps diagnosis separate from repair.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason:
- Deletion test: the test should be changed, not the code. FR-07 requires cancelled appointments to be retained as history. so a test expecting deletion contradicts the requirement. That is a test defect. The code should keep the same object with CANCELLED status, still findable and listed (as our F8-02 regression test checks).
- Different-practitioner conflict test: this does not reflect AC-04.2. AC-04.2 allows a different practitioner to be booked at the same time only the same practitioner conflicts (AC-04.1). A test expecting a conflict here is also a test defect and should be corrected to expect the booking to succeed.
Reason: expected behaviour comes from the requirements not from the current code or an existing test. A failing test is only correct if its expectation matches a requirement so check the requirement before deciding whether to fix the test or the code.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:
Smells and small refactorings (one at a time, tests run after each):
- Long method (70 lines): extract small, well-named helper methods (e.g a conflict check, a participant lookup).
- Four nested conditionals: use guard clauses (check and raise early) to flatten the nesting.
- Duplicate status strings (magic strings): use the existing `AppointmentStatus` enum.
- Direct collection manipulation (misplaced responsibility): go through the existing `SmartCareDataStore` methods (`add_appointment`, `find_appointment`, `list_appointments`, `has_practitioner_conflict`) instead of touching its dictionaries.
- Printing inside the service (mixed responsibility): return results or raise exceptions and let the console layer do the printing, so any required user-facing messages still appear.
- Validation mixed into the method, rely on the existing domain constructor and store validation rather than repeating it.

Classification:
- Rename `appt` to `appointment` — refactoring (clearer name, same behaviour).
- Extract a repeated conflict helper — refactoring (removes duplication, same behaviour).
- Add rescheduling — feature (new behaviour, out of scope for Stage 8).
- Restore retained cancellation lookup — repair (fixes the F8-02 defect so behaviour matches FR-07/FR-08).
- Replace a magic status string with the existing enum — refactoring (our section H change).

Behaviour that must remain unchanged: the same stored objects are returned (identity), the same exceptions are raised (ValueError for invalid values or conflicts, LookupError for missing records), the conflict rule (same practitioner and time rejected, different practitioner allowed), the guarded SCHEDULED into CANCELLED transition, and no state change when an operation fails. The full test suite passing before and after each change is the check.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason:
Failure: `tests/test_services.py::test_cancelled_appointment_remains_retrievable` on prepared commit 2d4b8df.
- Exception: `LookupError: Appointment not found`, raised at `smartcare/services.py` line 136.
- Test line: `tests/test_services.py` line 361, `found = clinic.appointments.find_appointment('A1')`, after booking and cancelling A1.
- Expected: the same A1 object returned with status CANCELLED, still in `list_appointments()`. Observed: LookupError, so the assertions on lines 362–364 never ran.
- Call path: test (line 361): `AppointmentService.find_appointment` (services.py line 134 calls the store)  `SmartCareDataStore.find_appointment` returns None: services.py line 136 raises LookupError.
- Requirement: FR-07 / AC-05.2 (cancelled history retained), FR-08 (lookup), BR-07 (guarded cancellation).

Ranked causes:
1. Store lookup filters out cancelled appointments (best fit: the store returned None, and `find_appointment` contains a status check). Check: after cancelling, call `store.find_appointment('A1')` directly and inspect its code. None plus the filter confirms it.
2. Cancellation deletes or replaces the appointment. Check: after cancelling, look at `store.list_appointments()`. If A1 is there as the same object with CANCELLED status, it was not deleted.
3. The service looks up the wrong ID or uses a different store. Check: confirm the service passes 'A1' to its own `data_store` and compare with a direct store lookup on the same store.
Result: check 2 showed A1 still stored and CANCELLED and check 1 showed the store returning None, so cause 1 was confirmed (copilot_check_f8_02.py).

Why a traceback alone is not enough: it shows where the exception was raised (services.py line 136), not why. The service only reported the None it received the cause was earlier, in `data_store.py`. Finding the cause needs checks that tell the possible explanations apart.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?
Response and reason: Where a failure shows up is often not where it is caused, so changing code straight away usually means fixing the wrong thing. In our F8-02 failure the traceback pointed to services.py line 136, but the cause was in data_store.py. Editing the service would have hidden the symptom, not fixed it. Guessing can also introduce new bugs, change correct behaviour, or tempt you to weaken a correct test just to get it passing. Reproducing the failure, checking the requirement, forming a hypothesis and testing it first means the fix targets the real root cause, stays small, and can be proved with a regression test.


Classification responses (1–5, each with reason): see A.1 — 1 symptom, 2 hypothesis (disproved), 3 evidence, 4 opinion, 5 evidence of location only (actual line services.py 136).
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: see A.2 (F8-01 same-practitioner booking), with the full record in sections C and E.
Traceback — exception/assertion; expected/observed; values test line; call path requirement; ranked causes and discriminating checks: see A.5 (`test_cancelled_appointment_remains_retrievable`, LookupError at services.py line 136, root cause in data_store.py `find_appointment`).

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [b8029b0. Requirements: SmartCare A3 Requirements Baseline 2026, revision 2.]
- Baseline test command / working directory / observed result / evidence: [python '-m pytest -q' in 'project/` on b8029b0 74 passed.]
- Clean preparation SHA if a record-only commit followed Stage 7: [Not applicable.]
- Branch and preparer / how teammates obtained this branch: [`debug/stage08`, prepared by Lachlan O'meara and pushed to GitHub. Teammates ran `git fetch` and `git switch debug/stage08`.]
- Downloaded tool version, source SHA256 and --check outcome: prepare_debugging.py version 1.1 (tool file SHA256 CD9A6786CD9FB518376716FB15A33BE63CCBB80282600B453FBF6095B3754F30), kept outside the repository on the Desktop. Baseline data_store.py SHA256 986c5445532ffd1d85e88639b6b6f34b84e15b2bbfc1882511a96938c3b641f6. --check: run once before --apply (PowerShell history) and did not report REFUSED; exact output not retained.
- --apply and --verify output summaries / artefact references: Commands run in order --check, --apply, --verify, each once (PowerShell history). --apply completed: `project/.stage8_faults/record.json` shows tool_version 1.1, git_sha b8029b0, status "prepared", fault data_store.py SHA256 1e804f451b1a9de42c67a38be9a9696029946ec6eb2319d37171fe5ba7a117f0. --verify: run after --apply; exact output not retained. The expected F8-01 and F8-02 failures were then confirmed by the test suite (7 failed, 67 passed).
- Bounded diff inspected and recovery location (not committed): [`git diff --stat b8029b0 2d4b8df` shows only `project/smartcare/data_store.py` changed (find_appointment and has_practitioner_conflict bodies). Backup and record.json in `project/.stage8_faults/`, ignored by .gitignore, not committed.]
- Prepared faulty-state commit SHA: [2d4b8df332ccc49259b652bbf1a57bc16eaaeb55 (`2d4b8df`, "Prepare stage 08 Debug", 2026-11-06 08:56).]
- Preparation or recovery issues and resolution, if any: [None. restore was not needed record.json still shows status "prepared".]
- Initial prepared full-suite command / result / key failures: [`python -m pytest -q` in `project/` on 2d4b8df, 7 failed, 67 passed. Conflict failures (`test_same_practitioner_same_time_conflict_is_rejected`: DID NOT RAISE ValueError) and cancellation failures ( `test_cancelled_appointment_remains_retrievable`: LookupError: Appointment not found).]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [Booking D1 twice at 9:00 on 1 Oct 2026 is accepted. No error.]
- Expected behaviour and requirement: [: The second booking should be rejected with ValueError (FR-05, AC-04.1). A different practitioner at that time should be allowed (AC-04.2).]
- Minimal synthetic reproduction steps: Register P1, P2, D1 and D2. Book A1 (P1, D1, 9:00). Book A2 (P2, D1, 9:00).
- Meaningful failing test path/name and exact relevant failure: [tests/test_regressions.py::test_f8_01_same_practitioner_same_time_rejected_without_change, which fails with “DID NOT RAISE ValueError”.]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [`has_practitioner_conflict` (data_store.py line 110) compared practitioner IDs with `!=` instead of `==`, so it detected other practitioners' bookings instead of the same practitioner's. Called directly after booking A1 (D1, 09:00), it returned False for D1 and True for D2 (copilot_check_f8_01.py), ruling out the service layer.]
- Smallest justified fix / diff / why other behaviour is preserved: [Changed `!=` to `==` on line 110 only. The other conditions (excluded ID, same time, SCHEDULED status) are unchanged, so cancelled bookings still don't block a slot and the check still changes nothing.]
- Repair SHA / focused verification result: [1ad49a2. `python -m pytest -q tests/test_regressions.py` in `project/`, 1 failed, 1 passed (F8-01 passes F8-02 not yet repaired).]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [After cancelling A1, store.find_appointment('A1') returns None.]
- Expected behaviour and requirement: [A cancelled appointment stays stored and findable, with CANCELLED status (FR-07, FR-08, AC-05.2).]
- Minimal synthetic reproduction steps: [Register P1 and D1. Book A1. Cancel A1. Look up A1.]
- Meaningful failing test path/name and exact relevant failure: tests/test_regressions.py::test_f8_02_cancelled_appointment_is_retained_and_found, which fails with "assert None is <Appointment>".
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [`find_appointment` (data_store.py lines 89–96) skipped any appointment with status "cancelled", so cancelled appointments stayed stored but could not be found. After cancelling A1, it was still in `list_appointments()` as the same object with CANCELLED status, but `store.find_appointment('A1')` returned None and the service raised LookupError (copilot_check_f8_02.py). Nothing was deleted.]
- Smallest justified fix / diff / why other behaviour is preserved: [Replaced the loop and status filter with a direct lookup, `self._appointments.get(required_text(appointment_id, 'Appointment ID'))`, matching `find_patient` and `find_practitioner`. Blank IDs still raise ValueError, missing IDs still return None, and repeated cancellation is again rejected with ValueError by the domain `cancel()` method]
- Repair SHA / focused verification result: [9084282.  `python -m pytest -q tests/test_regressions.py` in `project/`, 2 passed. Full suite, 76 passed.]

## E. Human-first hypotheses

### F8-01 human entry
Likely cause and why plausible: The practitioner ID check in `has_practitioner_conflict` is likely inverted (`!=` instead of `==`), so the method looks for other practitioners' bookings instead of the same practitioner's
Evidence intended to inspect / competing explanation / discriminating check: I will inspect the comparison in `has_practitioner_conflict`, the arguments `book_appointment` passes to it, and the F8-01 test result, which fails because the second D1 booking is accepted. A competing explanation is that the store method is correct and the service layer passes the wrong ID or skips the check. To tell these apart, book D1 at 09:00 and call `has_practitioner_conflict` directly. If it returns False for D1 and True for D2, the fault is in the store method. If it returns the correct results, the fault is in the service.
Member and saved sequence/time or commit showing this preceded consultation: [Lachlan O'Meara commit ba0b30cd4ef16eadffeecd5b61e6b257b1d0fab2 ]

### F8-02 human entry
Likely cause and why plausible: [`find_appointment` likely filters out cancelled appointments with the condition `status.value != "cancelled"`, so lookup returns `None` even though the appointment is still stored. This is plausible because a cancelled appointment would then seem to disappear, even though nothing removed it from the store.]
Evidence intended to inspect / competing explanation / discriminating check: [I will inspect the loop condition in `find_appointment`, how `cancel_appointment` changes the stored appointment, and the F8-02 test result, which fails because `find_appointment('A1')` returns `None` after cancelling. A competing explanation is that `cancel_appointment` deletes or replaces the appointment instead of only changing its status. To tell these apart, cancel A1 and check `list_appointments()`. If the same object is still listed with CANCELLED status, the fault is the lookup filter. If it is missing or replaced, the fault is in `cancel_appointment`.]
Member and saved sequence/time or commit showing this preceded consultation: [Lachlan O'Meara commit b9ee9441a5c424fe9c7cabac666e49c60ada99ef ]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [prompt: Observed behaviour: Booking A2 for practitioner D1 at 2026-10-01 09:00 succeeds even though A1 is already SCHEDULED for D1 at that time. Booking a different practitioner (D2) at that time is wrongly rejected.
Expected behaviour: FR-05/AC-04.1 reject the same practitioner at the same time AC-04.2 allow a different practitioner.
Steps to reproduce: register P1, P2, D1, D2 book A1 (P1, D1, 09:00) book A2 (P2, D1, 09:00).
Failing test: tests/test_regressions.py::test_f8_01_same_practitioner_same_time_rejected_without_change - "DID NOT RAISE ValueError"
My hypothesis: The practitioner ID check in has_practitioner_conflict is likely inverted (!= instead of ==), so the method looks for other practitioners' bookings instead of the same practitioner's. A competing explanation is that the store method is correct and the service layer passes the wrong ID or skips the check.
Relevant code (project/smartcare/data_store.py):
    def has_practitioner_conflict(
        self,
        practitioner_id: str,
        date_time: datetime,
        exclude_appointment_id: str | None = None,
    ) -> bool:
        for appointment in self.list_appointments():
            if (appointment.appointment_id != exclude_appointment_id
                    and appointment.practitioner.practitioner_id != practitioner_id
                    and appointment.date_time == date_time
                    and appointment.status.value == "scheduled"):
                return True
        return False
Task: Rank the three most likely causes. For each, identify the evidence I should inspect to distinguish it from the other possible causes. Do not rewrite the entire application. Do not invent requirements. Treat all suggested explanations as hypotheses.

output:Practitioner comparison is inverted (strongest directly supported by the code). In has_practitioner_conflict, the condition tests whether the stored appointment’s practitioner ID is != practitioner_id. That skips D1’s existing booking when checking another D1 booking, but treats D1’s booking as a conflict when checking D2, matching both observations. Inspect that comparison, then check test_same_practitioner_same_time_conflict_is_rejected and test_different_practitioner_same_time_is_allowed in test_services.py.

The service passes the wrong conflict-check arguments or mishandles the result (possible, but the inspected code argues against it). Inspect the call in services.py: confirm it passes the requested practitioner ID and time, and that a True result raises ValueError. A breakpoint or spy on has_practitioner_conflict during the two bookings would distinguish this from a faulty predicate: capture its arguments and return value for D1 and D2.

The runtime data or loaded module differs from what the report assumes (lower likelihood). Inspect list_appointments() after A1 is booked: its practitioner ID, exact datetime, and status should be D1, 09:00, and SCHEDULED. Also confirm the test is importing the edited workspace’s smartcare.data_store. This would distinguish a state/import mismatch from a logic defect the current source already shows checks for exact time and SCHEDULED status.

The first hypothesis is the best fit: the current predicate explains both the accepted D1 duplicate and rejected D2 booking. These are ranked hypotheses, not a request to change code.]
1. Ranked suggestion: the practitioner comparison in `has_practitioner_conflict` is inverted (`!=` instead of `==`). / Evidence check: inspect the comparison on data_store.py line 110 and call the store method directly after booking A1 for D1 at 09:00 (stage08/copilot_check_f8_01.py). / Observed evidence: line 110 used `!=` `has_practitioner_conflict('D1', 09:00)` returned False (expected True) and `('D2', 09:00)` returned True (expected False), matching both symptoms. `test_same_practitioner_same_time_conflict_is_rejected` and `test_different_practitioner_same_time_is_allowed` also failed. / Correct. / Accept: confirmed by the code and the direct call, and it explains both the accepted D1 duplicate and the rejected D2 booking.
2. Ranked suggestion: the service passes the wrong arguments to the conflict check or mishandles its result. / Evidence check: inspect `book_appointment` in services.py and compare with the direct store call. / Observed evidence: services.py passes `practitioner.practitioner_id` and `date_time` and raises ValueError when the result is True, which is correct. The direct store call, with no service involved, already returned the wrong results. / Wrong. / Reject: the fault reproduces without the service, so the service is not the cause.
3. Ranked suggestion: runtime data or the loaded module differs from what is assumed. / Evidence check: print `list_appointments()` after booking A1 and print where `smartcare.data_store` is loaded from. / Observed evidence: A1 stored with D1, 2026-10-01 09:00, SCHEDULED, as expected module loaded from the workspace's `project/smartcare/data_store.py`. / Wrong. / Reject: the data and module are correct, so they do not explain the failure.
Final human conclusion and comparison with initial hypothesis: The root cause is the inverted practitioner comparison (`!=` instead of `==`) on data_store.py line 110, so the method detected other practitioners' bookings instead of the same practitioner's. This matches my initial section E hypothesis. Copilot ranked the same cause first, but it was accepted only after the direct store call returned False for D1 and True for D2, which also ruled out the service-layer explanation I listed as the competing cause. Copilot's other two suggestions were checked and rejected using the evidence above.

### F8-02 Copilot review
Actual prompt / output reference and member: promt: Observed behaviour: After booking and cancelling A1, store.find_appointment('A1') returns None and the service find_appointment raises LookupError. A1 is still in store.list_appointments().
Expected behaviour: FR-07/FR-08/AC-05.2 — a cancelled appointment is retained and findable as the same object with CANCELLED status.
Steps to reproduce: register P1, D1 book A1 (P1, D1, 2026-10-01 09:00) cancel A1 call store.find_appointment('A1').
Failing test: tests/test_regressions.py::test_f8_02_cancelled_appointment_is_retained_and_found - "assert None is <Appointment>"
My hypothesis: find_appointment likely filters out cancelled appointments with the condition status.value != "cancelled", so lookup returns None even though the appointment is still stored. A competing explanation is that cancel_appointment deletes or replaces the appointment instead of only changing its status.
Relevant code (project/smartcare/data_store.py):
    def find_appointment(self, appointment_id: str) -> Appointment | None:
        if not isinstance(appointment_id, str) or not appointment_id.strip():
            raise ValueError("Appointment ID cannot be blank")
        for appointment in self.list_appointments():
            if (appointment.appointment_id == appointment_id.strip()
                    and appointment.status.value != "cancelled"):
                return appointment
        return None
Task: Rank the three most likely causes. For each, identify the evidence I should inspect to distinguish it from the other possible causes. Do not rewrite the entire application. Do not invent requirements. Treat all suggested explanations as hypotheses.

output: The store lookup excludes cancelled appointments (strongest). In data_store.py, find_appointment returns a matching ID only when appointment.status.value != "cancelled". That condition filters out A1 precisely when its status is CANCELLED. Inspect the stored A1 after cancellation: if it is the original object and its status is CANCELLED, this confirms the lookup filter as the cause. The existing retained-history assertions in test_services.py also specify that cancelled appointments remain findable.

Cancellation leaves A1 in an unexpected state or replaces it (weaker). The list may contain an appointment under A1, but that alone does not establish it is the original object with CANCELLED status. Compare the listed object with the object returned by booking (is), and inspect its ID and status after cancellation. If it is the original object with CANCELLED status, this hypothesis is ruled out. The current domain cancellation method changes status without deleting the appointment.

Lookup uses a different ID, store instance, or loaded implementation (least likely). Compare the queried ID with the stored appointment ID, check that the store used for list_appointments() is the same one used for find_appointment(), and confirm the test imports this project’s smartcare.data_store. These checks distinguish a lookup-context mismatch from the status filter. Because the store-level lookup itself returns None, the service’s LookupError is likely a consequence, not the primary cause: services.py raises it when the store returns None. These remain hypotheses until the object’s post-cancellation identity/status and lookup path are checked.
1. Ranked suggestion: `find_appointment` excludes cancelled appointments through the condition `appointment.status.value != "cancelled"`. / Evidence check: inspect the loop condition in data_store.py `find_appointment` after cancelling A1, check the stored object and call `store.find_appointment('A1')` directly (stage08/copilot_check_f8_02.py). / Observed evidence: the condition skips any appointment with status "cancelled". After cancelling, A1 was still stored as the original object with status CANCELLED, but `store.find_appointment('A1')` returned None, and the service then raised LookupError: Appointment not found. / Correct. / Accept: the code and the direct store call both confirm it. The service LookupError is a consequence of the store returning None, not a separate cause.
2. Ranked suggestion: cancellation leaves A1 in an unexpected state or replaces it with a different object. / Evidence check: after cancelling, compare the listed object with the booked object using `is`, and check its ID and status. / Observed evidence: `booked in store.list_appointments()` was True, the listed object `is` the original booked object, and its ID and status were A1 and CANCELLED. The domain `cancel()` method only changes status there is no delete method. / Wrong. / Reject: the appointment was retained correctly, which rules this out and also rules out the "removal path" idea from tutorial A.1.
3. Ranked suggestion: lookup uses a different ID, store instance or loaded implementation. / Evidence check: confirm the same store is used for listing and lookup, the ID queried matches the stored ID, and print where `smartcare.data_store` is loaded from. / Observed evidence: the script used one store for both calls with ID 'A1', which matched the stored appointment's ID the module was loaded from the workspace's `project/smartcare/data_store.py`. / Wrong. / Reject: the lookup context was correct, so the only remaining explanation is the status filter.
Final human conclusion and comparison with initial hypothesis: The root cause is the status filter in `find_appointment` (data_store.py lines 89–96), which hid cancelled appointments from lookup although they were still stored. This also made a repeated cancel raise LookupError instead of ValueError. This matches my initial section E hypothesis. Copilot ranked the same cause first, but it was accepted only after the check showed A1 still stored as the same CANCELLED object while the store lookup returned None, which also ruled out my competing explanation that cancellation deleted or replaced it. Copilot's other two suggestions were checked and rejected using the evidence above.

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
Actual change / diff / separate refactor SHA: [One line changed: `appointment.status.value == "scheduled"`, `appointment.status is AppointmentStatus.SCHEDULED`. Refactor commit:0c10c78]
Focused and full after-refactor commands / working directory / results / evidence: [`python -m pytest -q tests/test_regressions.py`, 2 passed `python -m pytest -q`, 76 passed.]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [Accepted. The same 76 tests pass before and after, with no test changes, so behaviour is preserved and the code is clearer.]


## I. Git, human review and integration

Issues for both defects / refactor scope and owners: #7 F8-01 practitioner conflict check inverted and #8 F8-02 cancelled appointments not found (Lachlan O'Meara), created after the repairs were merged in PR #4 to record them #9 refactor, replace "scheduled" magic string with enum (Lachlan O'Meara), resolved by PR #10. Earlier issues #2 and #3 are from previous stages.
Branch / prepared, repair and refactor checkpoints: `debug/stage08`. Prepared 2d4b8df (B) failing regression tests c5200cf (G) human hypotheses ba0b30c, b9ee944, 416099d (E) Copilot evidence c1f82ec (F) F8-01 repair 1ad49a2 (C) F8-02 repair 9084282 (D) refactor plan 74483eb (H) refactor 0c10c78 (H).
PR link and another member's reviewer identity: Repairs: PR #4 https://github.com/BenP64/st1-assignment-3/pull/4, merged without a formal review. Refactor: PR #10 https://github.com/BenP64/st1-assignment-3/pull/10, reviewed by Ben Parnell.
Key human feedback, difference from Copilot findings and response/outcome: PR #4 received no review feedback before merging. PR #10: Ben Parnell commented "Looks good. The tests pass correctly." No changes were requested, so none were made. Unlike Copilot, which only suggested possible causes, the reviewer checked the actual change and confirmed the tests pass.
Actual review approval / merge evidence: PR #4 merged by Ben Parnell on 2026-11-07 15:21 (merge commit 645aaef), no recorded approval. PR #10 approved  by Ben Parnell and merged by him on 2026-11-09 13:33 (merge commit 1b151a2).
Integrated code SHA and team pull/retest command / working directory / result: 1b151a284f159da2d3fd4b56ba2dbce15e80366b (`1b151a2`). `git switch main`, `git pull`, then `python -m pytest -q` in `project/`/ Lachlan O'Meara: 85 passed Ben Parnell: 85 passed. Repairs were first integrated at 645aaef (76 passed) the higher count at 1b151a2 includes Stage 9 tests merged into main in between.
Evidence-only later SHA / explanation if different: 74483eb (section H plan) changed only the stage08 record and was integrated with PR #10. 68f8c4e completes this record after the merge it changes only stage08/stage08_activities_and_evidence.md, and the code is unchanged since 1b151a2.
Each member's substantive contribution and artefact: Lachlan O'Meara: all Stage 8 engineering regression tests (c5200cf), human hypotheses (ba0b30c, b9ee944, 416099d), Copilot review and evidence (c1f82ec), F8-01 and F8-02 repairs (1ad49a2, 9084282), refactor (74483eb, 0c10c78), issues #7–#9 and the Stage 8 record. Ben Parnell: reviewed PR #10, merged PRs #4 and #10, and ran the integrated retest.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence?
None in our case. Copilot's first-ranked cause was correct for both defects, and we only accepted it after our own checks confirmed it. The least well-supported suggestion was its third for each defect: that the runtime data, loaded module or store instance was different from what we assumed (F8-01 #3, F8-02 #3). It sounded technical and confident, but nothing in the failure output pointed to it. Our check scripts showed the data was as expected, the same store was used, and the correct `project/smartcare/data_store.py` was loaded, so we rejected it.
2. What evidence changed your group's view? Our initial hypotheses were right, but the evidence moved them from "likely" to "confirmed" and ruled out the competing explanations. For F8-01, calling `has_practitioner_conflict` directly returned False for D1 and True for D2, proving the fault was in the store method and not the service. For F8-02, A1 was still in `list_appointments()` as the same object with CANCELLED status while `store.find_appointment('A1')` returned None, proving nothing was deleted and the lookup filter was the cause. The traceback had pointed to services.py line 136, but this evidence showed the root cause was in data_store.py.

3. How did regression tests protect the refactoring? 
We ran the full suite before and after replacing `"scheduled"` with `AppointmentStatus.SCHEDULED`, with no test changes: 76 passed both times. The F8-01 regression test checks that the same practitioner is still rejected and a different practitioner is still allowed, and `test_cancelled_booking_does_not_occupy_the_slot` checks that only SCHEDULED appointments block a slot. If the refactor had compared against the wrong status or broken the check, those tests would have failed, so passing them shows behaviour was preserved.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Reproduce the failure with a small example, check the requirement for the expected behaviour, form a hypothesis and gather evidence to test it. For example, we wrote failing regression tests and recorded our hypotheses before touching data_store.py.

2. Where should expected behaviour come from during debugging?

Response: From the requirements (e.g. FR-05, FR-07, AC-04.1), not from what the current code or an existing test happens to do. Tests can be wrong too.

3. What is a debugging hypothesis?

Response: A testable explanation for why a failure happens, with a check that can confirm or rule it out. For example: "find_appointment filters out cancelled appointments", checked by confirming A1 was still stored while lookup returned None.

4. What is a regression test and why is it retained?

Response: A test that reproduces a fixed defect and checks the correct behaviour. It is kept permanently so that if the defect comes back later, for example during a refactor, the test fails straight away.

5. What is meant by root cause?

Response: The underlying reason a failure occurs, as opposed to where it shows up. For F8-02 the error appeared in services.py, but the root cause was the status filter in data_store.py find_appointment.

6. What is refactoring?

Response: Changing the internal structure of code to make it clearer or simpler without changing its external behaviour, checked by tests passing before and after. For example, replacing "scheduled" with AppointmentStatus.SCHEDULED.

7. What is a swallowed exception?

Response: An exception that is caught and then ignored (e.g. an empty except block), so the error is hidden instead of reported or handled. It makes failures harder to find.

8. What is a code smell?

Response: A sign in the code that suggests a deeper problem or poor structure, such as duplication, long methods, magic strings, unclear names or misplaced responsibility. It is not necessarily a bug.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As hypotheses, not answers. Each suggestion should be checked against code, test results and requirements, then accepted, modified or rejected based on that evidence. Confident wording is not proof, and Copilot does not replace human diagnosis or review.

10. What is the Stage 8 engineering rule?

Response: Diagnose before you fix: use requirements, execution and code evidence to find the cause, make the smallest repair, keep a regression test, and only refactor while tests pass.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, feedback resolution and integrated retest recorded.
- [x] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [x] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: Integrated code SHA 1b151a2 (PR #10 merge, 85 passed). Submitted SHA 68f8c4e: it only adds the completed stage08 record, and the code is unchanged since 1b151a2.
Unresolved issues or incomplete checks / owner / next action: PR #4 (repairs) was merged on 2026-11-07 without a human review the refactor in PR #10 was reviewed by Ben Parnell, and in future a reviewer will approve before merging (owner: Lachlan O'Meara). Stage 9 work was merged into main before the Stage 8 refactor was integrated.
Handover note: Both Stage 8 defects are repaired and covered by retained regression tests in project/tests/test_regressions.py. Cancellation keeps history and the practitioner conflict rule is restored. The refactor uses AppointmentStatus.SCHEDULED in the conflict check. Evidence check scripts are in stage08/. Session-only storage remains the scope.
