# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Friday 8:30 Tutorial Group-1 

Members and responsibilities:
U3328698 - IzayahB: Stage 9
U3333375 - BenP64: Stage 7
U3329873 - Lachlano07: Stage 8
U3294151 - aadhya305: Stage 6

Stage 8 integrated SHA: `645aaef24ed6b04772dea439bf992d7395f1a447` (pending confirmation against `main`)
Command: `python -m pytest`
Working directory: `project/`
Actual result: 76 tests passed in 1.01 seconds, using Python 3.14.7 and pytest 8.3.5. All existing tests passed before Stage 9 modifications began.

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity |Required session/domain state |Needed to identify registered patients and link appointments to them. |
| Appointment history |Required session/domain state |Cancelled appointments must remain retrievable during the session (FR-07). |
| Temporary menu choice |Transient state |Only needed to determine which operation the user selected. |
| Practitioner specialty |Required session/domain state |Part of the practitioner's registered information (FR-03). |
| Debug print output |Transient state |Used during debugging, not part of the application's stored records. |
| Appointment status |Required session/domain state |Tracks whether an appointment is SCHEDULED, CANCELLED or COMPLETED. |

What is intentionally lost on exit? SmartCare stores its data in memory during the current session. When the program exits, all registered patients, practitioners and appointments are lost, including cancelled appointment history. Temporary menu choices and debug output are also not preserved. This is expected because persistence is outside the Stage 9 requirements.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key |appointment: Appointment |tuple[datetime, str] |Returns date/time and appointment ID for sorting. Does not modify anything. |Appointment.date_time and appointment_id. |
| select_appointments |appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus \| None |list[Appointment] |Filters by practitioner and optional status, returning a new sorted list. Assumes valid inputs. |Uses existing Appointment objects and the named sorting key. |
| Service listing |practitioner_id: str, status: AppointmentStatus \| None |list[Appointment] or error |Validates practitioner registration and status, retrieves appointments and delegates filtering to the query. |SmartCareDataStore, AppointmentStatus, QRY-04. |
| Console |Menu choice and text inputs (str) |Printed output; run_menu() -> None |Prompts, parses dates/status, calls services, displays results and recovers from expected errors. |Existing services, parse_date_time(), format_appointment(), UI-01/02. |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: Patient objects contain a unique patient ID and a required name. Practitioner objects contain a unique practitioner ID, name and specialty. Appointment objects contain a unique appointment ID, references to the actual registered Patient and Practitioner objects, a date_time and an AppointmentStatus enum. The domain classes enforce valid data and status transitions, while services coordinate registration, booking, cancellation and listing. Queries use these existing objects without modifying them, and the console handles user interaction.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input |Domain class is handling user interaction instead of just business rules. |The console should read user input. Appointment.cancel() should only validate and update appointment status. |
| Service prints/reads the menu |Service is mixing business logic with presentation. |console.py handles prompts and output. Services coordinate operations and return results or raise errors. |
| Query sorts its source in place |Using .sort() changes the original list, violating query purity. |queries.py should use sorted() to return a new list without modifying the source. |
| Store prints Appointment saved |The data store is handling presentation instead of data management. |The store should save and return the appointment object. The console should display the success message. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check:

| Behaviour | appointments.sort(key=appointment_sort_key) | result = sorted(appointments, key=appointment_sort_key) |
|---|---|---|
|Changes original list order? | Yes | No |
|Return value | None | New sorted list |
|Result identity | Same original list is modified | New list container, seperate from original |
|Suitable for a pure query? | No | Yes |

Meaningful mutation check:
original_order = appointments.copy()
result = sorted(appointments, key=appointment_sort_key)
assert appointments == original_order
assert result is not appointments


Score-example prediction and explanation of passing the named key:
[('Chen', 5), ('Ali', 8), ('Bea', 8)]

Explanation: The original list remains unchanged, with the result being a new list. The function sorts first by score, then by name to break ties. Passing key=score_key gives Python a reusable function reference, rather than calling it immediately. The appointment query uses the same idea with appointment_sort_key, sorting by date/time and then appointment ID.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion:

Cancellation changes an appointment''s status from SCHEDULED to CANCELLED without deleting the appoinment object, preserving the appintment history during the session (required by FR-07).

To confirm this, I cancelled appointment A1 and attempted to retrieve it with the 'find appointment' option. It still appeared, but with the status CANCELLED. I also listed D1's appointment with a blank status filter and confirmed that A1 was included. Filtering by SCHEDULED however, exluded A1 as it was no longer scheduled. 

I also successfully booked a new appointment, A3, at the same time for D1, confirming that cancellation of an appointment frees up the time slot while retaininng the appointment history.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: 

Stage 9 used sorted() rather than .sort() to avoid modifying the original appointment list. The query returns a new list containing the Appointment objects, preserving the identity and history. The server also validates practitioner ID's and status filters before handing it to the query.

During implementation and testing, an incorrect practitioner attribute reference and console cancellation issue were identified and corrected.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
|QRY-01 |Appointment list, practitioner ID |select_appointments filters by practitioner |Only matching practitioner appointments returned |test_practitioner_filter_and_id_tie_break |
|QRY-02 |Appointment list, optional status |Query filters using AppointmentStatus |None includes all; enum filters matching statuses |test_appointment_status_filtering |
|QRY-03 |Appointment dates and IDs |appointment_sort_key and sorted() |Ascending date/time, then ID; source unchanged |test_appointments_sorted_by_date_time, tie-break test |
|QRY-04 |Practitioner ID, optional status |AppointmentService.list_practitioner_appointments |Empty list for known no-match; appropriate errors for invalid/unknown |Two Stage 9 service tests |
|FP-01 |Explicit query arguments |Pure functions in queries.py |No hidden state, I/O or mutation |Code inspection and query tests |
|FP-02 |Empty, sorted or unsorted lists |select_appointments |New list containing original objects |test_query_returns_fresh_lists |
|FP-03 |Appointment object |appointment_sort_key |Reusable (date_time, appointment_id) key |Query sorting tests and code inspection |
|FR-01–03 |Patient/practitioner IDs, names, specialty |Registration and lookup services |Registered records found, duplicates rejected |Existing service tests and console demonstration |
|FR-04–05 |Appointment ID, participant IDs, datetime |Booking service |Booking succeeds or conflicts are rejected |test_complete_appointment_workflow |
|FR-06–08 |Appointment ID and status |Cancellation and lookup services |Scheduled appointment cancelled but remains retrievable |Workflow test and manual demonstration |
|FR-09 |Practitioner ID, status |Service listing and pure query |Filtered, correctly ordered appointments |Query and service tests |
|UI-01 |Repeated menu choices and inputs |run_menu() |Complete workflow within one session |Manual console demonstration |
|UI-02 |Invalid IDs, dates, statuses and choices |Console with service validation |Errors recover; no partial state changes |test_console_error_recovery and manual checks |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: 

Known practitioners with no appointments return an empty list. Unknown IDs raise LookupError, while invalid IDs or statuses raise ValueError. The console converts status text to an AppointmentStatus enum, with blank meaning all statuses.

Queries return new lists which contain the original Appointment objects, keeping identity and cancellation history preserved. Rejected operations leave records unchanged, and the console handles errors without ending, allowing users to continue.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
|QRY-03 |queries.py |Appointments sorted by date/time; original list unchanged |Passed |[Query tests](../project/tests/test_queries.py) |
|QRY-01, QRY-03 |queries.py |Correct practitioner selected; equal-time appointments sorted by ID |Passed |[Query tests](../project/tests/test_queries.py) |
|FP-01, FP-02 | queries.py|Repeated queries return fresh lists without modifying original objects|Passed |[Query tests](../project/tests/test_queries.py) |
|QRY-02 |queries.py |Default includes all statuses; explicit filters select correct appointments |Passed |[Query tests](../project/tests/test_queries.py) |
|QRY-04, FR-07 |services.py |Empty results, sorting, status filtering and cancelled history |Passed |[Service tests](../project/tests/test_services.py) |
|QRY-04 |services.py |Unknown/invalid IDs and invalid status rejected without changing records |Passed |[Service tests](../project/tests/test_services.py) |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O:

`select_appointments` is pure because it only uses inputs supplied to it, does not access a global store, and performs no input/output. It uses `sorted()` to return a new list without modifying the original list or Appointment objects. The named `appointment_sort_key` ensures consistent ordering.

What the tests do and do not establish:

The tests confirm filtering, sorting, fresh lists, object identity, status handling and error validation for the tested cases. However, passing tests cannot guarantee correctness for every possible input or prove purity alone. Inspecting code and integrated workflow testing will provide additional verification.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow |Register P1, D1, D2; book A1; attempt conflicting booking; book A2 with D2; cancel and find A1; list statuses; book A3 in freed slot; exit |Conflicts rejected, cancellation history retained, filtering correct, freed slot reusable |Main workflow tested successfully. Console cancellation dispatch bug was discovered and corrected. |[Console workflow evidence](stage09_evidence/console-workflow.txt) |
| UI-02 invalid-input recovery |Invalid menu choice, duplicate/blank ID, unknown participant, malformed/impossible date, invalid status and repeated cancellation |Errors displayed without crashing or changing valid records |Automated console recovery test passed. Manual verification of the complete error sequence still needs recording. |[Console workflow evidence](stage09_evidence/console-workflow.txt) |
| Automated service workflow |test_complete_appointment_workflow |Booking, conflict rejection, cancellation, retrieval, filtering and freed-slot booking work Test passed; rejected conflicting booking left the stored appointment list unchanged |[Automated workflow tests](../project/tests/test_workflows.py) |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: Sections A and B document the design and responsibility decisions. 
Actual prompt/context supplied: [Copilot review](stage09_evidence/copilot-review.md)
Actual response: [Copilot review response](stage09_evidence/copilot-review.md)

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
|Console tests lacked lookup and multi-appointment ordering checks.|Workflow tests|Optional|Accept - improves console coverage without changing production code.| Added test_console_lookup_and_listing_order.|Focused workflow tests and full regression suite passed.|

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: 

Domain classes enforce validation and cancellation rules. The shared store maintains registered objects and appointments. Services coordinate operations and validation, while pure queries filter and sort without changing data. The console handles user input, output and error recovery without duplicating business rules.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail?

The main architectural concern was ensuring all services shared the same data store while keeping responsibilities separate. The console handles user interaction, services manage operations, and queries handle filtering and sorting without changing the stored data.

2. Which Copilot suggestion did you reject as over-engineering, and why? 

I didn't reject any Copilot suggestions as the only recommendation was to improve console test coverage, which I accepted. I avoided unnecessary features such as databases or additional frameworks because they are outside Stage 9 requirements.

3. How did you prove cancelled appointments remain retrievable and listable in the same session?

I cancelled appointment A1 and confirmed it was still retrievable with CANCELLED status. It appeared in the all-status listing but not the SCHEDULED only listing. I also successfully booked A3 in the freed time slot.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? 

It uses only inputs explicitly given to it and returns a new sorted list without modifying the existing data. The purity would break if changes to the original list, printing or reading inputs occured.

2. Which explicit inputs are needed, and why avoid a global store? 

Appointment list, practitioner ID and optional status filter are needed. Avoiding a global store makes it easier to test and prevents hidden dependencies.

3. How can a new list reuse Appointment objects safely? 

The query creates a new list containing references to the existing Appointment objects without modifying them, preserving object identity.

4. Why use a named key, and what breaks equal-time ties?

appointment_sort_key allows for reusable, consistent sorting. Appointments are sorted by date/time first, then appointment ID when times are equal.

5. How do default and explicit status filters differ?

The default None filter includes all statuses. An explicit AppointmentStatus filter returns only appointments matching that status.

6. How do empty, unknown practitioner and invalid filter cases differ? 

A registered practitioner with no matches returns an empty list. An unknown practitioner raises LookupError, while an invalid status filter raises ValueError.

7. Which console errors recover, and how is unchanged state checked?

Invalid IDs, duplicate registrations, booking conflicts, incorrect dates, invalid statuses and unknown menu choices should recover. Tests compare stored records before and after rejection and confirm following valid operations succeed.

8. What is data integrity for registered participants, conflicts and history?

Appointments must reference registered patients and practitioners. Conflicting  bookings are rejected, and cancelled appointments remain stored and are retrievable during the session.

9. What is Copilot's review role, and who verifies findings? 

Copilot suggested possible improvements and identifies risks. Group members independently review its findings, decide whether to accept them and verify changes through testing.

10. How do pure functions and OOP responsibilities work together? 

Domain objects maintain business rules, services coordinate operations, and pure functions filter and sort data without modifying it. The console handles interaction without controlling domain rules.

## H. Review, completion and common handover

Issues and bounded branches: 
Branch: [stage09-queries](https://github.com/BenP64/st1-assignment-3/tree/stage09-queries)
GitHub Issue: Pending / not yet created.

PR/diff and another-member human reviewer: 
PR: Pending — Stage 9 branch not yet submitted for review.
Human reviewer: Pending — another group member to review.

Review responses and Copilot comparison:
[Copilot review](stage09_evidence/copilot-review.md)
Copilot found no Critical or Important issues but suggested
improving console test coverage. I accepted the suggestion
and added test_console_lookup_and_listing_order.
The focused and full test suites passed.
Human PR review: Pending.

Integrated common Stage 9 SHA: Integrated common Stage 9 SHA:
Pending — Stage 9 pull request review and merge into main.

Full regression command, working directory, actual count/result and evidence:
Working directory: `project/`
Command: `python -m pytest -q`
Actual result: 85 tests passed, including the Stage 9 query, service and workflow tests.
Evidence: [Query tests](../project/tests/test_queries.py), [Service tests](../project/tests/test_services.py), [Workflow tests](../project/tests/test_workflows.py).
Integrated verification: Pending after teammate review and merge.

README run instructions and scope/limitations: README run instructions and scope/limitations:
[Project README](../project/README.md)

Unresolved issues and support/action: 
No known unresolved code or test failures. All reported Stage 9 tests passed.
Pending actions: Complete teammate PR review, merge Stage 9 into main, rerun the full test suite and record the integrated SHA.
Support required: Group member review and approval before integration.

UG common candidate / PG future branch plan:
The completed Stage 9 work will be reviewed, merged into main and verified as the common candidate for the group.
The integrated Stage 9 SHA will be recorded and protected for Stage 12.

- [x] Query contracts, purity, new lists and named-key ordering verified.
- [x] Service empty/unknown/invalid cases and cancellation history verified.
- [x] Every console command and invalid-input recovery demonstrated.
- [x] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [x] Reflections and ten formative responses completed.
- [x] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
