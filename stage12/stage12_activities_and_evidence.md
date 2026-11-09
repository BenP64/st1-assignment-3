# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Fri 8:30, Group 1
Members and UG/PG applicability: Aadhya Singh (aadhya305), Ben Parnell (BenP64), Izayah Baker (IzayahB), Lachlan O'Meara (Lachlano07), All UG


## A Release scope and starting SHA

Release label/version and requirements baseline: ...
Common starting SHA / branch / applicable members: `ece879be0c9f53e32395b6c4f1a890cb0a3cb7fa` on main, all four members.
PG starting SHA / branch / applicable members or not applicable: Not applicable
Working-state review and approved integration: ...
Protected common candidate and PG differences: ...
Feature freeze / owner / verifier: ...


## B Requirements and release readiness matrix

**Tutorial activity 1:** All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: ...

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope                        | Evidence                                                                                                         | Location/link and SHA                                                                                                                                                                                                                                                   | Reviewer | Sufficient? | Gap/action                                     |
|------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|-------------|------------------------------------------------|
| Cancellation history works (FR-07, AC-05.2), common        | Tests check the cancelled appointment is the same object, is CANCELLED, can still be found.                      | [test_services.py](../project/tests/test_services.py) `test_cancelled_appointment_remains_retrievable`, `test_stage9_service_listing_and_history`; [test_regressions.py](../project/tests/test_regressions.py) `test_f8_02_cancelled_appointment_is_retained_and_found` | Ben      | Yes         | None                                           |
| Architecture responsibilities are appropriate, common      | Code inspection and Stage 9 Copilot review, which found no critical or important issues                          | [smartcare/](../project/smartcare/), [copilot-review.md](../stage09/stage09_evidence/copilot-review.md)                                                                                                                                                                 | Ben      | Yes         | Small quality issues found                     |
| Rescheduling is safe — PG only                             | Not applicable                                                                                                   | N/A                                                                                                                                                                                                                                                                     | N/A      | N/A         | N/A                                            |
| AI use is responsible — common recheck / PG assurance      | Copilot decisions recorded in Stage 7 H, Stage 8 E/F and Stage 9 E                                               | [Stage 7](../stage07/stage07_activities_and_evidence.md), [Stage 8](../stage08/stage08_activities_and_evidence.md), [Stage 9](../stage09/stage09_activities_and_evidence.md)                                                                                            | Ben      | Yes         | None                                           |
| System is maintainable                                     | 85 tests, a shared `clinic` fixture, small focused classes, a named sort key                                     | [tests/](../project/tests/)                                                                                                                                                                                                                                             | Ben      | Yes         | Some minor style warnings                      |
| FR-01–03 register/find and validation                      | ST-01, ST-03, ST-04, TD-01 to TD-05, TS-01 to TS-11                                                              | [Stage 7 record](../stage07/stage07_activities_and_evidence.md) section B, [test_services.py](../project/tests/test_services.py)                                                                                                                                        | Ben      | Yes         | None                                           |
| FR-04–05 booking/conflict rules                            | ST-02, ST-05 to ST-07, TS-12 to TS-20, `test_f8_01_same_practitioner_same_time_rejected_without_change`          | [test_services.py](../project/tests/test_services.py), [test_regressions.py](../project/tests/test_regressions.py)                                                                                                                                                      | Ben      | Yes         | None                                           |
| FR-06–08 cancellation/history/find                         | ST-08, TD-13 to TD-15, TS-16, TS-21 to TS-26, F8-02 regression test                                              | [test_domain.py](../project/tests/test_domain.py), [test_services.py](../project/tests/test_services.py)                                                                                                                                                                | Ben      | Yes         | None                                           |
| FR-09 and QRY/FP listing/filter/order/purity               | 4 query tests (sorting, practitioner filter + ID tie-break, fresh lists, status filter), 2 service listing tests | [test_queries.py](../project/tests/test_queries.py), [test_services.py](../project/tests/test_services.py) `test_stage9_service_listing_*`                                                                                                                              | Bem      | Yes         | None                                           |
| UI full console sequence and error recovery (UI-01, UI-02) | 3 workflow tests and the Stage 9 console transcript                                                              | [test_workflows.py](../project/tests/test_workflows.py), [console-workflow.txt](../stage09/stage09_evidence/console-workflow.txt)                                                                                                                                       | Ben      | Yes         | The live Stage 12 demo still needs to be done. |
| Session-only scope / FR-10 retired                         | No persistence code, the README says so and the console prints "Session data is not saved" when you exit         | [project/README.md](../project/README.md) Limitations, [console.py](../project/smartcare/console.py) `run_menu`                                                                                                                                                         | Ben      | Yes         | None                                           |
| PG RES and assurance integration                           | Not applicable                                                                                                   | N/A                                                                                                                                                                                                                                                                     | N/A      | N/A         | N/A                                            |


## C Full regression results

| Suite/scope                              | Environment/version                                               | Working directory and command   | Tested SHA | Actual result       | Evidence link               |
|------------------------------------------|-------------------------------------------------------------------|---------------------------------|------------|---------------------|-----------------------------|
| Complete common                          | Python 3.13.18, pytest 8.3.5                                      | project/, `python -m pytest -q` | `ece879b`  | 85 passed, 0 failed | [tests/](../project/tests/) |
| Complete PG if applicable                | Not applicable                                                    | N/A                             | N/A        | N/A                 | N/A                         |
| Affected focused checks after correction | No code was changed in Stage 12, so there was nothing to re-check | N/A                             | N/A        | N/A                 | N/A                         |
| Full integrated recheck                  | Python 3.13.18, pytest 8.3.5                                      | project/, `python -m pytest -q` | `ece879b`  | 85 Passed, 0 failed | ...                         |
Prior assertions preserved / reviewed test diff: No earlier assertions were removed. test_starter.py hasn't changed since Stage 6.


Remaining failure / limitation: No failing tests. The limitations are shown in G.


## D Console and end to end demonstration
The table below shows what the console printed when we ran these inputs at `ece879b` with `python main.py --interactive`.

| Demo step                                                        | Synthetic setup/input                                                                                                                                                                                                                       | Expected requirement           | Observed result                                                                                                                                                                                  | Evidence/link                                                                                                |
|------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Problem and stakeholders                                         | SmartCare is a simple clinic appointment system. Reception staff register patients and practitioners and book or cancel appointments. Practitioners need a correct list of their appointments. The clinic manager needs no double bookings. | Course release scope           | Explained in the demo                                                                                                                                                                            |                                                                                                              |
| Register and find Patient and two Practitioners                  | Menu 1: P1 "John Smith". Menu 2: P1. Menu 3: D1 "Jane Doe" General, D2 "Fake User" General. Menu 2: P404                                                                                                                                    | FR-01, FR-02, FR-03, UI-02     | "Registered patient: P1", "Patient: P1 - John Smith", D1 and D2 registered. Unknown patient gives "Error: Patient not found" and the menu comes back                                             |                                                                                                              |
| Valid booking                                                    | Menu 5: A1, P1, D1, 2026-12-01 09:00                                                                                                                                                                                                        | FR-04, AC-03.1                 | "Booked: A1: P1 with D1, 2026-12-01 09:00, scheduled"                                                                                                                                            |                                                                                                              |
| Same practitioner exact-time conflict rejected                   | Menu 5: A2, P1, D1, 2026-12-01 09:00                                                                                                                                                                                                        | FR-05, AC-04.1                 | "Error: Practitioner already has a SCHEDULED appointment at this time". Menu 7 A2 gives "Appointment not found", so nothing partial was saved                                                    |                                                                                                              |
| Different practitioner same time allowed                         | Menu 5: A3, P1, D2, 2026-12-01 09:00                                                                                                                                                                                                        | FR-05, AC-04.2                 | "Booked: A3: P1 with D2, 2026-12-01 09:00, scheduled"                                                                                                                                            |                                                                                                              |
| Cancel SCHEDULED and retain/find CANCELLED object                | Menu 6: A1, then menu 7: A1                                                                                                                                                                                                                 | FR-06, FR-07, AC-05.1, AC-05.2 | "Cancelled: A1 ... cancelled", then find shows "A1: P1 with D1, 2026-12-01 09:00, cancelled"                                                                                                     |                                                                                                              |
| Invalid/repeated cancellation rejected                           | Menu 6: A1 again, menu 6: A404                                                                                                                                                                                                              | AC-05.3                        | "Error: Only SCHEDULED appointments may be cancelled", "Error: Appointment not found"                                                                                                            |                                                                                                              |
| Default all-status listing                                       | Menu 8: D1, blank status                                                                                                                                                                                                                    | FR-09, QRY-02, QRY-04          | Shows A1 (cancelled), so the default includes every status                                                                                                                                       |                                                                                                              |
| Explicit filtering / empty vs unknown / deterministic order      | Menu 8: D1 "scheduled" gives "No matching appointments." Menu 8: D9 gives "Error: Practitioner not found". Equal-time ordering is shown with tests                                                                                          | QRY-01 to QRY-04               | Empty list and unknown practitioner are handled differently. Ordering by date/time then ID is checked by `test_practitioner_filter_and_id_tie_break` and `test_console_lookup_and_listing_order` | [test_queries.py](../project/tests/test_queries.py), [test_workflows.py](../project/tests/test_workflows.py) |
| Invalid date/status/menu/lookup recovery and continued operation | Status "xyz", date "2026-13-01 09:00", menu choice 9, then a valid booking                                                                                                                                                                  | UI-02                          | "'xyz' is not a valid AppointmentStatus", "Invalid calendar date/time", "Invalid menu choice", then the next booking works                                                                       |                                                                                                              |
| Session-only limitation and normal exit                          | Menu 0                                                                                                                                                                                                                                      | FR-10 retired                  | "Goodbye! Session data is not saved." Restarting the program starts empty                                                                                                                        |                                                                                                              |
| One meaningful requirement-linked pytest test explained          | `python -m pytest tests/test_services.py::test_cancelled_appointment_remains_retrievable`                                                                                                                                                   | FR-07, AC-05.2                 | 1 passed. It checks the found object `is` the booked one, its status is CANCELLED and it's still in `list_appointments()`. It doesn't prove the console shows it correctly                       | [test_services.py](../project/tests/test_services.py)                                                        |
| Architecture and one actual AI decision / known limitation       | Show smartcare/ files. AI decision: in Stage 7 we rejected Copilot's repeated-cancel test because it would have used `pytest.raises(Exception)`                                                                                             | Architecture, responsible AI   | Domain, store, services, queries and console each have one job. Limitation: all data is lost on exit                                                                                             | [Stage 7 H/I](../stage07/stage07_activities_and_evidence.md)                                                 |
| PG reschedule identity/participants/time and no-op               | Not applicable                                                                                                                                                                                                                              | N/A                            | N/A                                                                                                                                                                                              | N/A                                                                                                          |
| PG conflict/invalid status/failure non-mutation                  | Not applicable                                                                                                                                                                                                                              | N/A                            | N/A                                                                                                                                                                                              | N/A                                                                                                          |
| PG old slot / current lookup/list ordering / assurance risks     | Not applicable                                                                                                                                                                                                                              | N/A                            | N/A                                                                                                                                                                                              | N/A                                                                                                          |


**Stable demo owner / fresh process / command:** Ben Parnell. Fresh process from project/: `python main.py --interactive`.


**PG demonstrations through service/tests or not applicable:** Not applicable.


## E Final code quality and AI review

| Review area                                                     | Code/evidence location                                                                                                         | Finding or no finding                                                                                                                                                                                                                                    | Correction/no change and recheck |
|-----------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| OOP responsibilities and pure-query boundaries                  | domain.py, data_store.py, services.py, queries.py, console.py                                                                  | No finding. Appointment owns cancel(), services do the conflict check using the shared store, queries.py uses `sorted()` with explicit inputs and no input/output, and the console only handles input and output                                         | No change                        |
| PascalCase and snake_case naming                                | all of smartcare/                                                                                                              | No finding. Classes are PascalCase (e.g. `SmartCareDataStore`) and functions and variables are snake_case                                                                                                                                                | No change                        |
| Useful type hints and meaningful docstrings                     | services.py line 156, console.py line 73, main.py lines 1 and 10, queries.py line 1, data_store.py `has_practitioner_conflict` | Finding. Some docstrings still say "Stage 9: implement..." or "intentionally incomplete menu", and the docstring for `has_practitioner_conflict` was removed in Stage 8. The two Stage 9 tests in test_services.py are missing the `-> None` return hint | No change                        |
| Four-space indentation and imports/layout                       | pycodestyle run over smartcare/, main.py and tests/                                                                            | Finding. No tabs, four-space indents. About 30 minor warnings, mostly long lines and missing blank lines.                                                                                                                                                | No change                        |
| Focused methods / duplication / dead or commented code          | main.py line 5 `# this is a test`, main.py `except NotImplementedError`                                                        | Finding. A leftover test comment, and the `NotImplementedError` branch can't happen any more because run_menu is finished                                                                                                                                | No change                        |
| Globals / leakage / unnecessary inheritance or frameworks       | all of smartcare/                                                                                                              | No finding. No globals, the only inheritance is `AppointmentStatus(Enum)`, standard library only                                                                                                                                                         | No change                        |
| No SQLite/persistence/repository ABCs/speculative features      | all of smartcare/                                                                                                              | No finding. No SQL, files or repository classes                                                                                                                                                                                                          | No change                        |
| Synthetic data / secrets / dependencies / provenance            | requirements-dev.txt, all tracked files                                                                                        | Mostly no finding. The only dependency is `pytest==8.3.5` (PyPI, MIT licence) and the app uses only the standard library. All names are fake ("John Smith"). Finding: student IDs are in the Stage 6 and Stage 8 records, see H                          | Recorded in H                    |
| Significant common Copilot contributions and human verification | Stage 7 H, Stage 8 E/F, Stage 9 E                                                                                              | See the table below                                                                                                                                                                                                                                      | See the table below              |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST           | Not applicable                                                                                                                 | N/A                                                                                                                                                                                                                                                      | N/A                              |

| AI claim                                                                                       | Affected requirement/code            | Human check                                                                                                                       | Accept/Modify/Reject and reason                    | Actual outcome/action or no change                    |
|------------------------------------------------------------------------------------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|-------------------------------------------------------|
| Stage 7: Copilot's candidate test for repeated cancellation                                    | FR-06, AC-05.3                       | Compared it with our TS-23. It didn't expect ValueError or check state after                                                      | Reject, our test was stronger                      | TS-23 kept, passes                                    |
| Stage 8: F8-01 is caused by an inverted practitioner comparison in `has_practitioner_conflict` | FR-05, AC-04.1, data_store.py        | Matched Lachlan's hypothesis recorded before asking Copilot (commit ba0b30c). Checked by the failing then passing regression test | Modify                                             | Fixed in 1ad49a2, `test_f8_01_...` passes             |
| Stage 8: F8-02 is caused by `find_appointment` filtering out cancelled appointments            | FR-07, FR-08, AC-05.2, data_store.py | Matched Lachlan's hypothesis recorded before asking Copilot (commit b9ee944). Checked by the failing then passing regression test | Modify                                             | Fixed in 9084282, `test_f8_02_...` passes             |
| Stage 9: console tests didn't check find options or multi-appointment order                    | UI-01, QRY-03, test_workflows.py     | Checked the existing console test                                                                                                 | Accept, it adds coverage without changing app code | Added `test_console_lookup_and_listing_order`, passes |


**Access route or approved equivalent / limitations:** GitHub Copilot, Microsoft Copilot in browser.


**Available AI evidence and missing evidence honestly disclosed:** Copilot prompts and outputs are in Stage 7 H, Stage 8 F, [stage08_copilot_notes.md](../stage08/stage08_copilot_notes.md) and [copilot-review.md](../stage09/stage09_evidence/copilot-review.md). 


## F README and reproducibility check

| README item                                                   | Location                        | Verifier | Result/gap                                                                                                                                                                            |
|---------------------------------------------------------------|---------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Purpose and included common/PG scope                          | project/README.md               | Ben      | Gap. The "Stage 9" section lists the features, but the top of the file still says "SmartCare Stage 6 starter" and that the TODOs raise NotImplementedError, which isn't true any more |
| Out-of-scope capabilities and known limitations               | project/README.md "Limitations" | Ben      | Partly. Session-only data is there. Out-of-scope items (logins, notifications, billing, clinical advice) aren't listed                                                                |
| Confirmed teaching Python version and dependency installation | README.md, project/README.md    | Ben      | OK. Python 3.13 with pytest 8.3.5 and `python -m pip install -r requirements-dev.txt`                                                                                                 |
| Working directory / demo / interactive / test commands        | README.md, project/README.md    | Ben      | OK. `cd project`, `python main.py`, `python main.py --interactive`, `python -m pytest -q`                                                                                             |
| Repository structure and architecture responsibilities        | project/README.md               | Ben      | Partly. Domain, store and services are described, but queries.py, console.py and the folder layout aren't                                                                             |
| Responsible AI summary / synthetic-data rule                  | README.md                       | Ben      | Partly. The synthetic-data rule is there. There's no summary of how we actually used Copilot                                                                                          |
| Release label/version and SHA links                           | README.md "Group index"         | None     | Gap. Repo URL, latest stage, verified SHA and final SHA are ...                                                                                                                       |


**Root README index and project/README verified:** All stage record links in the root README work. The group index and project/README need the gaps above fixed.


**Fresh clone or extracted ZIP / candidate identity: Pre-check:** `git archive` ZIP of `ece879b`, extracted into an empty folder. It contains README.md, .gitignore, project/ and all the stage folders, and no .git folder.


**Verifier and clean environment / actual version:** ...


**Setup/run/test commands and observed results:** `python -m pip install -r requirements-dev.txt` installed pytest 8.3.5. `python main.py` printed "A1: P1 with DR1, 2026-10-01 09:00, scheduled". `python main.py --interactive` then 0 exited normally. `python -m pytest -q` gave 85 passed.


**Missing local file or setup gap / remedy and recheck:** No missing files, everything ran from the ZIP alone. The README content gaps above need fixing and re-checking.


## G Known limitations debt and release notes

**Delivered features:** Register and find patients and practitioners, book appointments with exact-time practitioner conflict checking, cancel while keeping history, find appointments, list a practitioner's appointments with an optional status filter, sorted by date/time then ID, and an interactive console menu that recovers from bad input.


**Important fixes:** F8-01, same-practitioner clashes were allowed and other practitioners were wrongly blocked (fixed in 1ad49a2). F8-02, cancelled appointments couldn't be found (fixed in 9084282). Stage 9: console cancellation and a wrong practitioner attribute were fixed during implementation.


**Architecture/quality improvements:** Pure query functions with a named sort key, one shared SmartCareDataStore used by all services, and the test suite growing from 8 to 85 tests with fixtures, parametrisation and regression tests.


**Known limitations:** Data only lasts for one session. Times are local and to the minute. Conflicts only count the exact same time. There's no rescheduling or completing appointments through the menu. Pressing Ctrl+D/Ctrl+Z at a prompt ends the program with an EOFError.


**AI-assisted development note:** GitHub Copilot was used to suggest test candidates (Stage 7), rank debugging hypotheses after we wrote our own (Stage 8) and review Stage 9 code. Every suggestion was checked by a person and with tests.

| Debt item                                                                                                                                               | Impact                                                                    | Priority | Future action                                            | Accepted? / release rationale |
|---------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|----------|----------------------------------------------------------|-------------------------------|
| `has_practitioner_conflict` uses the string `"scheduled"` instead of `AppointmentStatus.SCHEDULED`, has no docstring, and the enum import is now unused | Easy to break if the enum value changes.                                  | Low      | Use the enum again, add the docstring back, re-run tests | Accepted                      |
| Old "Stage 9 TODO"/"incomplete menu" docstrings, the `# this is a test` comment and the dead `NotImplementedError` branch in main.py                    | Confusing for the next developer, no effect on behaviour                  | Low      | Update the docstrings and remove the dead code           | Accepted                      |
| About 30 pycodestyle warnings (long lines, blank lines)                                                                                                 | Readability only                                                          | Low      | Tidy up with a formatter                                 | Accepted                      |
| EOFError if input ends (Ctrl+D/Ctrl+Z)                                                                                                                  | The program crashes instead of exiting cleanly. Not a current requirement | Low      | Catch EOFError in run_menu and exit normally             | Accepted                      |

**Session-only synthetic data and minute-precision local time:** All records are fake and are lost when the program exits. Times are local date/times to the minute, entered as `YYYY-MM-DD HH:MM`.


**Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions:** Not included. There are no logins or user roles, no patient portal, no SMS/email.


**Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations:** One user, one process, in-memory only. No timezone handling. No logging or monitoring. No usability or accessibility testing has been done.


**Difference between accepted scope limit and unresolved required behaviour:** The items above are deliberate scope limits that the requirements don't ask for. The README gaps in H are not debt, because the handout requires the README to be complete.


**PG assurance residual risks / owner / status or not applicable:** Not applicable.


## H Release findings and corrective action

| Requirement/claim                           | Reproduction/observation                                                                                                                                                       | Impact/severity                      | Owner/action                                 | Corrective diff | Focused/full recheck                | Residual limit                      |
|---------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|----------------------------------------------|-----------------|-------------------------------------|-------------------------------------|
| README complete (handout section 5)         | project/README.md still starts as the "Stage 6 starter" text. The root README group index still has empty fields. No out-of-scope list, structure, AI summary or version label | Medium, release condition            | Update both READMEs                          | ...             | Verifier re-runs F on a fresh copy  | ...                                 |
| No student IDs in Git (handout section 7)   | Student IDs in stage06, lines 7 to 9 and stage08, lines 99 and 104                                                                                                             | Medium, they would end up in the ZIP | Remove the IDs, keep GitHub usernames        | ...             | Re-run the grep, regenerate the ZIP | The IDs are still in older commits. |
| Previous stage recorded (handout section 1) | The Stage 8 record still has about 70 fields (A, B, C/D root cause and fix, F decisions, G after-repair rows, H, I, J, K)                                                      | Medium, evidence gap                 | Lachlan: finish the Stage 8 record           | ...             | N/A, records only                   | ...                                 |
| Review evidence (Stage 7 and 9)             | Stage 7 was pushed straight to main (b8029b0) with no PR. Stage 9 H says the review is "Pending", but PRs #5 and #6 were merged                                                | Low, evidence gap                    | Ben: Record who reviewed                     | N/A             | N/A                                 | ...                                 |
| Code quality (section E)                    | Magic string, unused import, old docstrings, test comment                                                                                                                      | Low, behaviour is correct            | Group decided not to change code in Stage 12 | None            | 85 passed at `ece879b`              | Recorded as debt in G               |


**Justified no-change conclusion if no defect found:** No product defects were found. All 85 tests pass, and the console run in D matched every expected result for FR-01 to FR-09 and UI-01 to 02. So no code was changed.


**Release blockers still open / status:** README completion, removing student IDs.a


## I Git review and integration evidence

**Issue / PR / diff links and reviewed SHA: Earlier work:** [PR #4](https://github.com/BenP64/st1-assignment-3/pull/4) (Stage 8 debug), [PR #5](https://github.com/BenP64/st1-assignment-3/pull/5) (Stage 9 queries), [PR #6](https://github.com/BenP64/st1-assignment-3/pull/6) (Stage 9 documentation). Stage 12 fixes: ...


**Independent reviewer / feedback / response:** ...


**Integration commit / full recheck:** ...


**Tracked and untracked file inspection / cleanliness:** `git ls-files` at `ece879b` shows 29 files. They're the READMEs, .gitignore, project/ source and tests, the stage records and the Stage 8/9 evidence files. No .venv, __pycache__, .pytest_cache, .idea or Stage 8 utility files, and .gitignore covers them.


**Secrets/staff material/caches/tool-metadata exclusion check:** No passwords, tokens or keys found.


**Candidate recovery plan / known-good SHA:** Known-good code SHA is `89b7fcc`. Recover with `git checkout <sha>` to inspect it, or `git revert` for a bad commit.


**Named substantive contributions:** Aadhya Singh, Stage 6: ([9271a40](https://github.com/BenP64/st1-assignment-3/commit/9271a404479c57fd1003f27dbc537b37b58395fa)). Ben Parnell, Stage 7: ([b8029b0](https://github.com/BenP64/st1-assignment-3/commit/b8029b0adb82d8beae7cb5de424037445a2cf552)). Lachlan O'Meara, Stage 8: ([PR #4](https://github.com/BenP64/st1-assignment-3/pull/4)). Izayah Baker, Stage 9: ([PR #5](https://github.com/BenP64/st1-assignment-3/pull/5), [PR #6](https://github.com/BenP64/st1-assignment-3/pull/6)). Ben Parnell, Stage 12: ...


## J Human release decision

**Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY:** READY WITH DOCUMENTED LIMITATIONS


**Approver / date / rationale and evidence:** Ben Parnell, 9/11/2026, All 85 tests pass on `ece879b` from a fresh zip with Python 3.13 and pytest 8.3.5


**What risks remain / conditions / owners:** All data is lost upon program close, Ctrl+D/Ctrl+Z crashes the code. 


**Can the team explain the system:** Yes, each member can explain their own stage and the system.


**Can a change be recovered:** Yes. Every stage is a commit on main, `89b7fcc`/`ece879b` is known-good, and a bad change can be undone with `git revert`.


**Common decision / PG decision where different:** Common only, not applicable.


## K Final tested release SHA

**Exact common tested SHA:** `ece879be0c9f53e32395b6c4f1a890cb0a3cb7fa`


**Exact PG tested SHA or not applicable:** Not applicable, UG-only group.


**Final submitted SHA / repository URL:** https://github.com/BenP64/st1-assignment-3


**Evidence-only later commit and difference explanation:** ...


**Executable changes after testing and re-verification:** None so far.


**Source ZIP name / SHA correspondence / extracted comparison:** ... (do `git archive --format=zip --output=../SmartCare-release.zip FULL_SUBMITTED_SHA`, extract it and compare it with the SHA)


## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [x] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [x] Independent human review, integration and release decision recorded.
- [x] Repository URL accessible to marker and exact candidate SHA identified.
- [x] One source ZIP from submitted commit with root README.md and .gitignore.
- [x] project/ source and all accumulated applicable tests included.
- [x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [x] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [x] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [x] Mixed-group common protection and candidate upload routing checked.
- [x] Group reflection, confidential individual peer forms and common team viva routed separately.

**Confirmed assessment item/upload route:** Completed

**Deadline/timezone:** 9/11/2026 11:59PM

**Repository access arrangement:** Completed

**Mixed-candidate upload arrangement:** ...

**Oral/video recording/accessibility arrangements:** Completed

**Remaining administration or release dependency:** ...


## M Formative questions

**1. What is a release candidate?** A specific version that is thought to be ready for release, which then gets tested and checked before official release.

**2. What is feature freeze and why is it used?** A feature freeze is when you stop adding new features, so you cna focus on fixing the current version instead of introducing new bugs.

**3. What is regression testing in a release context?** Regression testing is running all the tests again on the specific release candidate, to make sure recent changes haven't broken anything.

**4. What is a known limitation?** A known limitation is something the software doesn't do or can't handle, that is specified somewhere for users to know about it.

**5. What is technical debt?** Technical debt is shortcuts or messy code left in the project that still work but will make working on the program harder in the future.

**6. What are release notes?** Release notes are a short summary of what's in the release, fixes, known limitations, etc.

**7. What is software maintenance?** Software maintenance is everything done after release like bug fixes.

**8. What is the purpose of the individual demonstration/viva?** To show that each of us actually understands the system and our own part in it. 

**9. What should the final responsible-AI check establish before release?** That every AI suggestion we used was checked by a person, matches the requirements and doesn't contain and secrets.

**10. What is the main course conclusion about AI and the role of the software engineer?** AI can suggest code and tests, but people are still responsible for checking it and deciding what to accept.


## N Reflection viva and handover

**Strongest evidence SmartCare is ready:** 85 tests all pass from a fresh ZIP, and they're linked to every requirement.


**Weakest area:** The reviews, Stage 7 had no PR review.


**How AI use changed from Stage 1 to Stage 12:** The further we moved along in development of the program, especially during the testing phase, AI was introduced to suggest ideas to test.


**Start doing — engineering and AI use:**
  - **Engineering:** Open a PR with a reviewer for every change.
  - **AI:** Give AI the requirements and acceptance criterion for better responses.

**Stop doing — engineering and AI use:** ...
- **Engineering:** Pushing straight to main.
- **AI:** Stop letting AI add things the requirements don't ask for.

**Continue doing — engineering and AI use:** ...
- **Engineering:** Adding a regression test for every bug
- **AI:** Writing down our hypothesis or test ideas before asking AI


**What worked / caused rework / future delivery improvement:**
- **What worked:** Splitting the stages between group members.
- **What caused rework:** Stage 7 didn't completely match the test files.
- **Future improvement:** Have a second member review a PR before merging.


**One paragraph — If AI can write code why do we still need software engineers:** AI doesn't know if the code it writes is actually correct for the people using it. In this project Copilot suggested things that seemed fine but actually created more problems, e.g. creating a new patient when a lookup failed, and tests that would pass with any error. We only knew these were bad because we fully understood the requirements and the program. Engineers decide what the software should do, check that it actually does that, and then take the responsibility when releasing it. Unlike AI.

| Preparation item                                                                  | Own explanation and evidence link                                                                                                                                                                                                     |
|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Problem and stakeholders                                                          | A bad clinic appointment booking system. Reception staff, practitioners, clinic managers and patients.                                                                                                                                |
| Two requirements and acceptance criteria                                          | FR-05: AC-04.1, the same pracitioner at the exact same time is rejected, and AC-04.2, a different practitioner is allowed. FR-07: AC-05.2, a cancelled appointment can still be found.                                                |
| Domain model and architecture                                                     | Patient, practitioner and appointment are in domain.py, SmartCareDataStore holds the three dictionaries, the services coordinate use cases, queries.py does the filtering and sorting, and console.py handles the inputs and outputs. |
| Design trade-off                                                                  | Keeping everything in memory makes it simple and easy to test, but all the data is lost upon program exit.                                                                                                                            |
| Meaningful test and its limits / 100 percent coverage                             | `test_cancelled_appointment_remains_retrieveable` proves AC-05.2 for that case but it doesn't test the console. 100% coverage would onyl show what lines ran, not that the results are right.                                         |
| Diagnosed defect and verification                                                 | F8-02: `find_appointment` filtered out cancelled appointments. test_f8_02_... failed before the fix (c5200cf) and passed after it (9084282).                                                                                          |
| Shared store and session-state/query responsibilities                             | All three services use the same store object so they see the same records. Queries take the list as an input and return a new list.                                                                                                   |
| What would break if session-state lookup/query responsibilities changed?          | If each service has its own store, booking couldn't find registered patients. If the query sorted the store's list in place, it would change the store's order.                                                                       |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancelling only needs the appointment's own status, so it belongs in Appointment. A conflict needs to lok at other Appointments, so the service checks it using the sharde store.                                                     |
| FR-07 retained history test                                                       | `test_cancelled_appointment_remains_retrieveable` (TS-22)                                                                                                                                                                             |
| Actual AI change rejected/modified or honestly accepted with verification         | Stage 7: I rejected Copilot's repeated-cancel test because it used `pytest.raisese(Exception)` and didn't check the state afterwards.                                                                                                 |
| Unresolved limitation / future production work                                    | Session-only data. A real clinic would need saved data, logins, timezones, and better accessibility.                                                                                                                                  |
| Personal implementation contribution                                              | Ben Parnell: Stage 7 & Stage 12, Izayah Baker: Stage 9, Aadhya Singh: Stage 6,                                                                                                                                                        |                                                                                                                                                                                                                                                                   |
| PG agentic change and rescheduling verification                                   | Not applicable.                                                                                                                                                                                                                       |
| PG responsible-AI risk/remediation or supported no finding                        | Not applicable.                                                                                                                                                                                                                       |

#### Personal test / review / design / integration contribution


**Ben Parnell**
- **Test:** Wrote and tested stage 7's tests.
- **Review & Design:** Checked Copilot's three test suggestions and rejected them because our tests were better.
- **Integration:** Set up the group repo and merged all PRs into main.


**Izayah Baker**
- **Test:** Created query and workflow tests, verified console functionality and passed all 85 tests. 
- **Review & Design:** Documented Stage 9 design decisions, reviewed Copilot feedback and improved test coverage.  
- **Integration:** Pushed Stage 9 changes and verified the merged code on `main`.


**Aadhya Singh**
- **Test:** To confirm acceptance requirements, unit tests for valid patient searches, unknown patient IDs, and invalid/blank IDs were written and executed.
- **Review & Design** Reviewed the specifications for patient searches and made verified the procedure adhered to the service duty of retrieval only, without generating or altering patient information.
- **Integration:** Merged the patient search modifications with the main branch and confirmed that, following integration, all tests, both new and old, continued to pass. 

**Lachlan O'Meara**
- **Test:** Wrote the Stage 8 regression tests (`project/tests/test_regressions.py`) for F8-01 and F8-02, confirmed they failed for the right reasons before repair and passed after, and ran the full suite before and after each change (76 passed). Also wrote the Stage 6 appointment cancellation tests.
- **Review & Design:** Recorded my own hypotheses for both defects before using Copilot, then checked each of Copilot's six suggestions against evidence from check scripts and accepted or rejected them. Chose and justified the Stage 8 refactor (replacing the `"scheduled"` magic string with `AppointmentStatus.SCHEDULED`) without changing behaviour. Acted as the other-member reviewer in Stage 6.
- **Integration:** Prepared the Stage 8 debugging branch with the tutor's tool, made the two minimal repairs and the refactor as separate commits, created issues #7–#9, and integrated the work through PRs #4 and #10, then retested on `main`.

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: ...
Separate reflection / peer / common team viva evidence links and routing: ....
No further coding stage. Later corrections use the published assessment process.
