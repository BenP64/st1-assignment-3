# Stage 7 Testing and Verification Record

Group/tutorial: **Fri 8:30 Group 1** Members/cohorts: **Aadhya Singh, Ben Parnell, Izayah Baker, Lachlan O'Meara**
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement                         | Positive test                                                                 | Negative test                                         | Key assertion                                                                                                                                         |
|-------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-01 Register patient              | Register P2 in a fresh store that alreadys holds P1.                          | Register "P1" again, with a different name.           | Positive: store.find_patient('P2') is the returned patient. Negative: ValueError is raised AND store.find_patient('P1') is still the original object. |
| FR-05 Prevent practitioner conflict | Book D2 at 09:00 while D1 already has a scheduled booking.                    | Book D1 again at exactly 09:00 while A1 is SCHEDULED. | Positive: second booking is stored and SCHEDULED. Negative: ValueError, and store.list_appointments() == [first]                                      |
| FR-06 Cancel appointment            | Cancel a SCHEDULED appointment through AppointmentService.cancel_appointment. | Cancel the same appointment a second time             | Positive: returned object is the booked appointment and its status is AppointmentStatus.CANCELLED. Negative: ValueError and the status is unchanged.  |
| FR-07 Retain cancelled history      | After cancelling A1, look it up by ID and list all appointments.              | Look up an appointment ID that was never booked.      | Positive: find_appointment('A1') is the original object, status CANCELLED, and it is still in list_appointments(). Negative: LookupError.             |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak, Why: It can never fail, so it proves nothing about any behaviour; it only shows the line was reached without an earlier exception.

`assert appointment is not None`
Judgement: Weak, Why: It shows something was returned, but not that it is the right appointment. So a wrong object would still pass.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong, Why: It checks the exact required state change for AC-05.1.

`assert len(results) > 0`
Judgement:  Weak, Why: Any non-empty list passes, including the wrong records, wrong practitioner or wrong order.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong, Why: It proves the store holds and returns that exact object under ID A1.

### Activity 3 Boundary thinking

- **Blank identifiers:** `''` and `'   '` as patient/practitioner/appointment ID : `ValueError`, nothing stored. `' P1 '` trims to `'P1'`, so it is a duplicate of an existing P1. Contract: "IDs are strings, trimmed, non-blank and case-sensitive"
<br></br>
- **Whitespace-only names/specialty:** `'   '` for name or specialty raises a `ValueError`. e.g. `'  Alex Example  '` is accepted and stored trimmed. Contract: "Required names and specialty are non-blank."
<br></br>
- **Same-time practitioner bookings:** same practitioner at exactly 09:00, existing SCHEDULED raises a `ValueError`. Different practitioner at 09:00 is allowed. But same practitioner at 09:01 is allowed, because the rule is "exact time" and there is no duration-overlap rule.
<br></br>
- **Cancelled appointments:** a CANCELLED 09:00 booking for D1 does not block a new 09:00 booking for D1, the cancelled record also is still retrievable.
<br></br>
- **Invalid status transitions:** CANCELLED -> cancel again raises a `ValueError`, but stays CANCELLED. COMPLETED -> cancel, raises a `ValueError`, and stays COMPLETED.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate        | What is wrong                                                                                                              | Rewritten test intention                                                                                        |
|------------------|----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| 1 (not None)     | Only shows an object exists, a wrong or unstored object still passes.                                                      | Registering P2 stores it: store.find_patient('P2') is the returned patient and its name is the given name       |
| 2  (not None)    | For booking it does not check status, participants or storage.                                                             | Booking A1 stores a SCHEDULED appointment linked to the registered P1/D1 objects.                               |
| 3 (asserts True) | Cannot fail, so it verifies nothing.                                                                                       | Cancelling a SCHEDULED appointment changes its status to CANCELLED and returns the same object.                 |
| 4 (SMS)          | Invents a notification feature that is not in the requirements, it passes because it asserts something that doesn't exist. | Replace with an actual requirement: repeated cancellation raises ValueError and leaves the status CANCELLED     |
| 5   (SMS)        | Same invented-requirement problem, tests behaviour SmartCare does not have.                                                | Replace with an actual requirement: a cancelled appointment is still found by ID and listed in the same session |

### Tutorial exit question

**Why can 100% code coverage coexist with poor software verification?** <br></br>
Coverage only records which lines ran, not whether any assertion checked the right result. 

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement  | Acceptance criteria                                                                        | Test ID | Test type                                | Test name / location                                                                   | Expected behaviour                                  | Result / observed status | Supplied or student-authored |
|--------------|--------------------------------------------------------------------------------------------|---------|------------------------------------------|----------------------------------------------------------------------------------------|-----------------------------------------------------|--------------------------|------------------------------|
| FR-01        | Contract: "IDs are strings, trimmed, non-blank"                                            | ST-01   | Domain unit, negative                    | tests/test_starter.py::test_required_fields                                            | Blank patient ID / blank specialty raise ValueError | Passed                   | Supplied                     |
| FR-04        | AC-03.1, AC-06.1                                                                           | ST-02   | Service, positive                        | tests/test_starter.py::test_registration_and_booking                                   | Booking stored, SCHEDULED, linked objects           | Passed                   | Supplied                     |
| FR-01        | AC-01.2                                                                                    | ST-03   | Service, negative                        | tests/test_starter.py::test_duplicate_patient_preserves_original                       | Duplicate P1 rejected, original kept                | Passed                   | Supplied                     |
| FR-03        | BR-02                                                                                      | ST-04   | Service, negative                        | tests/test_starter.py::test_duplicate_practitioner_preserves_original                  | Duplicate D1 rejected, original kept                | Passed                   | Supplied                     |
| FR-04        | BR-03                                                                                      | ST-05   | Service, negative                        | tests/test_starter.py::test_duplicate_appointment_preserves_original                   | Duplicate A1 rejected, original kept                | Passed                   | Supplied                     |
| FR-04        | AC-03.2, BR-04/09                                                                          | ST-06   | Service + store, negative                | tests/test_starter.py::test_unregistered_participants_rejected                         | Unknown/lookalike participant rejected              | Passed                   | Supplied                     |
| FR-05        | AC-04.1, AC-04.2                                                                           | ST-07   | Service, negative + positive             | tests/test_starter.py::test_conflict_rule_and_different_practitioner                   | Same slot rejected; D2 allowed                      | Passed                   | Supplied                     |
| FR-06        | AC-05.1, AC-05.3 (domain only)                                                             | ST-08   | Domain via booked object                 | tests/test_starter.py::test_domain_cancellation_and_guard                              | cancel() changes status; repeat rejected            | Passed                   | Supplied                     |
| FR-01        | AC-01.1 (partial domain evidence)                                                          | TD-01   | Domain unit, positive                    | tests/test_domain.py::test_valid_patient_stores_trimmed_fields                         | Fields kept, trimmed                                | Passed                   | Student-authored             |
| FR-01        | Contract: "IDs are … trimmed, non-blank"                                                   | TD-02   | Domain unit, negative/boundary (5 cases) | tests/test_domain.py::test_blank_patient_id_is_rejected                                | ValueError for '', spaces, tab/newline, None, int   | Passed                   | Student-authored             |
| FR-01        | Contract: "Required names … are non-blank"                                                 | TD-03   | Domain unit, negative/boundary (3 cases) | tests/test_domain.py::test_blank_patient_name_is_rejected                              | ValueError                                          | Passed                   | Student-authored             |
| FR-03        | Partial domain evidence for FR-03                                                          | TD-04   | Domain unit, positive                    | tests/test_domain.py::test_valid_practitioner_stores_trimmed_fields                    | ID, name, specialty kept trimmed                    | Passed                   | Student-authored             |
| FR-03        | Contract: "Required names and specialty are non-blank"                                     | TD-05   | Domain unit, negative/boundary (6 cases) | tests/test_domain.py::test_blank_practitioner_fields_are_rejected                      | ValueError                                          | Passed                   | Student-authored             |
| FR-04        | AC-03.1 (partial: initial status)                                                          | TD-06   | Domain unit, positive                    | tests/test_domain.py::test_new_appointment_starts_scheduled                            | SCHEDULED; same participant objects/time            | Passed                   | Student-authored             |
| FR-04        | BR-04/09 (partial: object types)                                                           | TD-07   | Domain unit, negative                    | tests/test_domain.py::test_appointment_requires_real_participant_objects               | ValueError for IDs or swapped objects               | Passed                   | Student-authored             |
| FR-04        | Contract: "Timezone-aware values and nonzero seconds/microseconds are invalid"             | TD-08   | Domain unit, negative/boundary (5 cases) | tests/test_domain.py::test_invalid_appointment_time_is_rejected                        | ValueError                                          | Passed                   | Student-authored             |
| FR-04        | Contract: "local naive datetime values at minute precision"                                | TD-09   | Domain unit, boundary positive           | tests/test_domain.py::test_minute_precision_time_is_accepted                           | 23:59, zero seconds accepted                        | Passed                   | Student-authored             |
| FR-04        | BR-08                                                                                      | TD-10   | Domain unit, negative                    | tests/test_domain.py::test_non_enum_status_is_rejected                                 | ValueError for status text                          | Passed                   | Student-authored             |
| FR-06        | Contract: "identity fields are read-only"; "Cancellation uses the public domain operation" | TD-11   | Domain unit, negative                    | tests/test_domain.py::test_identity_and_status_are_read_only                           | AttributeError; values unchanged                    | Passed                   | Student-authored             |
| FR-06        | AC-05.1 (domain)                                                                           | TD-12   | Domain unit, positive                    | tests/test_domain.py::test_cancel_changes_status                                       | CANCELLED; other fields unchanged                   | Passed                   | Student-authored             |
| FR-06        | AC-05.3 (domain)                                                                           | TD-13   | Domain unit, negative                    | tests/test_domain.py::test_repeated_cancellation_is_rejected                           | ValueError; stays CANCELLED                         | Passed                   | Student-authored             |
| FR-06        | BR-06, BR-08                                                                               | TD-14   | Domain unit, negative                    | tests/test_domain.py::test_completed_appointment_cannot_be_cancelled                   | ValueError; stays COMPLETED                         | Passed                   | Student-authored             |
| FR-01        | AC-01.1                                                                                    | TS-01   | Service, positive                        | tests/test_services.py::test_register_patient_stores_and_returns_same_object           | Stored object is returned object                    | Passed                   | Student-authored             |
| FR-01        | AC-01.2, BR-01                                                                             | TS-02   | Service, negative/boundary (2 cases)     | tests/test_services.py::test_duplicate_patient_id_is_rejected_without_overwrite        | 'P1' and ' P1 ' rejected; original kept             | Passed                   | Student-authored             |
| FR-01        | Contract: "IDs are … case-sensitive"                                                       | TS-03   | Service, boundary positive               | tests/test_services.py::test_patient_ids_are_case_sensitive                            | 'p1' registered separately                          | Passed                   | Student-authored             |
| FR-01        | Contract: invalid inputs raise ValueError; NFR-01                                          | TS-04   | Service, negative (4 cases)              | tests/test_services.py::test_invalid_patient_registration_leaves_store_unchanged       | ValueError; store unchanged                         | Passed                   | Student-authored             |
| FR-02        | AC-02.1                                                                                    | TS-05   | Service, positive (2 cases)              | tests/test_services.py::test_find_known_patient_returns_stored_object                  | Same object, incl. trimmed ID                       | Passed                   | Student-authored             |
| FR-02        | AC-02.2                                                                                    | TS-06   | Service, negative                        | tests/test_services.py::test_find_unknown_patient_raises_lookup_error                  | LookupError; nothing created                        | Passed                   | Student-authored             |
| FR-02        | Contract: blank ID raises ValueError                                                       | TS-07   | Service, negative (2 cases)              | tests/test_services.py::test_find_patient_with_blank_id_raises_value_error             | ValueError                                          | Passed                   | Student-authored             |
| FR-03        | Supporting lookup: "return the registered practitioner"                                    | TS-08   | Service, positive                        | tests/test_services.py::test_find_known_practitioner_returns_stored_object             | Same object                                         | Passed                   | Student-authored             |
| FR-03        | Contract: "A valid unknown service lookup raises LookupError"                              | TS-09   | Service, negative                        | tests/test_services.py::test_find_unknown_practitioner_raises_lookup_error             | LookupError; nothing created                        | Passed                   | Student-authored             |
| FR-04, FR-08 | AC-03.1, AC-06.1, BR-04                                                                    | TS-10   | Service, positive                        | tests/test_services.py::test_book_appointment_stores_scheduled_appointment             | Stored, SCHEDULED, registered objects               | Passed                   | Student-authored             |
| FR-04        | AC-03.2                                                                                    | TS-11   | Service, negative (2 cases)              | tests/test_services.py::test_booking_unknown_participant_is_rejected                   | LookupError; nothing stored                         | Passed                   | Student-authored             |
| FR-04        | Datetime contract; NFR-01                                                                  | TS-12   | Service, negative (2 cases)              | tests/test_services.py::test_booking_invalid_time_is_rejected_without_storing          | ValueError; nothing stored                          | Passed                   | Student-authored             |
| FR-04        | BR-03                                                                                      | TS-13   | Service, boundary negative               | tests/test_services.py::test_duplicate_appointment_id_with_spaces_is_rejected          | ' A1 ' rejected; original kept                      | Passed                   | Student-authored             |
| FR-08        | Contract: unknown → LookupError, blank → ValueError                                        | TS-14   | Service, negative                        | tests/test_services.py::test_find_unknown_appointment_raises_lookup_error              | LookupError / ValueError                            | Passed                   | Student-authored             |
| FR-05        | AC-04.1, BR-05                                                                             | TS-15   | Service, negative                        | tests/test_services.py::test_same_practitioner_same_time_conflict_is_rejected          | ValueError; only first stored                       | Passed                   | Student-authored             |
| FR-05        | AC-04.2                                                                                    | TS-16   | Service, positive                        | tests/test_services.py::test_different_practitioner_same_time_is_allowed               | Both stored, SCHEDULED                              | Passed                   | Student-authored             |
| FR-05        | BR-05 "exact time"                                                                         | TS-17   | Service, boundary positive               | tests/test_services.py::test_same_practitioner_one_minute_later_is_allowed             | 09:01 booking allowed                               | Passed                   | Student-authored             |
| FR-05, FR-07 | BR-05 "SCHEDULED", AC-05.2                                                                 | TS-18   | Service, boundary positive               | tests/test_services.py::test_cancelled_booking_does_not_occupy_the_slot                | Slot rebooked; cancelled kept                       | Passed                   | Student-authored             |
| FR-06        | AC-05.1                                                                                    | TS-19   | Service, positive                        | tests/test_services.py::test_cancel_appointment_changes_status_and_returns_same_object | Same object, CANCELLED                              | Passed                   | Student-authored             |
| FR-07        | AC-05.2, BR-07                                                                             | TS-20   | Service, positive                        | tests/test_services.py::test_cancelled_appointment_remains_retrievable                 | Found and listed after cancel                       | Passed                   | Student-authored             |
| FR-06        | AC-05.3, BR-06                                                                             | TS-21   | Service, negative                        | tests/test_services.py::test_repeated_cancellation_is_rejected_without_change          | ValueError; still stored, CANCELLED                 | Passed                   | Student-authored             |
| FR-06        | BR-06, BR-08                                                                               | TS-22   | Service, negative                        | tests/test_services.py::test_completed_appointment_cancellation_is_rejected            | ValueError; stays COMPLETED                         | Passed                   | Student-authored             |
| FR-06        | Contract: unknown → LookupError, blank → ValueError; NFR-01                                | TS-23   | Service, negative                        | tests/test_services.py::test_cancel_unknown_or_blank_id_leaves_appointments_unchanged  | Errors raised; A1 stays SCHEDULED                   | Passed                   | Student-authored             |
## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criteria         | Positive/Negative/Boundary | Test intention                                       | Observable result expected                      | Added evidence beyond supplied tests                                  |
|---------|-------------|-----------------------------|----------------------------|------------------------------------------------------|-------------------------------------------------|-----------------------------------------------------------------------|
| TD-01   | FR-01       | AC-01.1 (partial)           | Positive                   | Construction keeps trimmed values                    | `patient_id == 'P1'`, `name == 'Alex Example'`  | Supplied tests never check trimming                                   |
| TD-02   | FR-01       | Validation contract         | Negative/Boundary          | Every kind of invalid ID is rejected                 | ValueError ×5                                   | Supplied checks only `' '`; adds empty, tab/newline, None, non-string |
| TD-03   | FR-01       | Validation contract         | Negative/Boundary          | Name is required                                     | ValueError                                      | Not covered by supplied tests                                         |
| TD-04   | FR-03       | Partial                     | Positive                   | Practitioner fields kept trimmed                     | Three trimmed fields                            | Not covered                                                           |
| TD-05   | FR-03       | Validation contract         | Negative/Boundary          | Each required field checked separately               | ValueError ×6                                   | Supplied checks only empty specialty                                  |
| TD-06   | FR-04       | AC-03.1 (partial)           | Positive                   | New appointment is SCHEDULED, keeps objects          | `status is SCHEDULED`, identity of participants | Isolates the domain rule from the service                             |
| TD-07   | FR-04       | BR-04/09 (partial)          | Negative                   | IDs or swapped objects are not accepted              | ValueError ×3                                   | Not covered                                                           |
| TD-08   | FR-04       | Datetime contract           | Negative/Boundary          | tz-aware, seconds, microseconds, text, None rejected | ValueError ×5                                   | Not covered                                                           |
| TD-09   | FR-04       | Datetime contract           | Boundary                   | Partner of TD-08: valid minute time accepted         | `date_time == edge`                             | Shows TD-08 rejects for the right reason                              |
| TD-10   | FR-04       | BR-08                       | Negative                   | Status must be an enum                               | ValueError                                      | Not covered                                                           |
| TD-11   | FR-06       | Read-only identity contract | Negative                   | Identity/status cannot be overwritten                | AttributeError; values unchanged                | Not covered                                                           |
| TD-12   | FR-06       | AC-05.1 (domain)            | Positive                   | cancel() changes only status                         | CANCELLED, other fields same                    | Supplied test does not check other fields                             |
| TD-13   | FR-06       | AC-05.3 (domain)            | Negative                   | Second cancel rejected                               | ValueError; still CANCELLED                     | Kept as required reference intention                                  |
| TD-14   | FR-06       | BR-06/08                    | Negative                   | COMPLETED cannot be cancelled                        | ValueError; still COMPLETED                     | Not covered                                                           |
| TS-01   | FR-01       | AC-01.1                     | Positive                   | Registration stores through the service              | Store returns same object                       | Supplied only registers inside a helper, never asserts it             |
| TS-02   | FR-01       | AC-01.2                     | Negative/Boundary          | Duplicate (incl. spaced) rejected                    | ValueError; original kept                       | Adds the trimmed duplicate case                                       |
| TS-03   | FR-01       | Case-sensitive contract     | Boundary                   | 'p1' is a distinct ID                                | Both stored separately                          | Not covered                                                           |
| TS-04   | FR-01       | Validation contract, NFR-01 | Negative                   | Bad registration leaves store unchanged              | ValueError; list unchanged                      | Not covered                                                           |
| TS-05   | FR-02       | AC-02.1                     | Positive                   | Lookup returns the stored object                     | `is clinic.patient`                             | Stage 6 TODO; not in supplied tests                                   |
| TS-06   | FR-02       | AC-02.2                     | Negative                   | Unknown ID reports absence                           | LookupError; nothing created                    | Stage 6 TODO                                                          |
| TS-07   | FR-02       | Validation contract         | Negative                   | Blank ID is a ValueError, not LookupError            | ValueError                                      | Checks the two error types are distinguished                          |
| TS-08   | FR-03       | Supporting lookup           | Positive                   | Lookup returns stored practitioner                   | `is clinic.doctor`                              | Stage 6 TODO                                                          |
| TS-09   | FR-03       | Lookup contract             | Negative                   | Unknown ID → LookupError                             | LookupError; nothing created                    | Stage 6 TODO                                                          |
| TS-10   | FR-04/08    | AC-03.1, AC-06.1            | Positive                   | Full booking evidence                                | SCHEDULED, registered objects, found by ID      | Adds date/time and list checks                                        |
| TS-11   | FR-04       | AC-03.2                     | Negative                   | Unknown patient and practitioner each block booking  | LookupError; nothing stored                     | Supplied checks unknown patient only                                  |
| TS-12   | FR-04       | Datetime contract           | Negative                   | Invalid time leaves no partial booking               | ValueError; empty list                          | Not covered                                                           |
| TS-13   | FR-04       | BR-03                       | Boundary                   | Spaced duplicate appointment ID rejected             | ValueError; original unchanged                  | Adds trimmed case                                                     |
| TS-14   | FR-08       | Lookup contract             | Negative                   | Unknown vs blank appointment ID                      | LookupError / ValueError                        | Not covered                                                           |
| TS-15   | FR-05       | AC-04.1                     | Negative                   | Exact conflict rejected without side effects         | ValueError; only first stored                   | Supplied test does not check state after rejection                    |
| TS-16   | FR-05       | AC-04.2                     | Positive                   | Other practitioner allowed                           | Both stored                                     | Adds list check                                                       |
| TS-17   | FR-05       | BR-05 exact time            | Boundary                   | One minute later is not a conflict                   | Booking stored                                  | Not covered                                                           |
| TS-18   | FR-05/07    | BR-05, AC-05.2              | Boundary                   | Cancelled booking frees the slot                     | Rebooking succeeds; old record kept             | Not covered                                                           |
| TS-19   | FR-06       | AC-05.1                     | Positive                   | Service cancel returns same object                   | `result is booked`, CANCELLED                   | Stage 6 TODO                                                          |
| TS-20   | FR-07       | AC-05.2                     | Positive                   | History retained after cancel                        | Found and listed                                | Stage 6 TODO                                                          |
| TS-21   | FR-06       | AC-05.3                     | Negative                   | Repeat cancel through service                        | ValueError; still stored                        | Stage 6 TODO                                                          |
| TS-22   | FR-06       | BR-06/08                    | Negative                   | COMPLETED cannot be cancelled via service            | ValueError; stays COMPLETED                     | Not covered                                                           |
| TS-23   | FR-06       | Cancel contract, NFR-01     | Negative                   | Unknown/blank ID error types, no side effect         | LookupError, ValueError; A1 SCHEDULED           | Not covered                                                           |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange                                                                  | Act                                                    | Assert                                                                                                     | Why meaningful / why assertion proves criterion                                                                                                   |
|---------|--------------------------------------------------------------------------|--------------------------------------------------------|------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| TD-02   | No state; one invalid ID value per parametrised case                     | `Patient(bad_id, 'Alex Example')`                      | `pytest.raises(ValueError)`                                                                                | Uses the specific documented exception, so a TypeError or silent acceptance would fail the test.                                                  |
| TD-12   | Fresh SCHEDULED appointment; keep references to its patient/practitioner | `appointment.cancel()`                                 | status `is CANCELLED`; ID, patient (`is`), practitioner (`is`), time unchanged                             | Proves the transition and that cancellation changes only status (BR-07).                                                                          |
| TD-14   | Appointment constructed with status COMPLETED                            | `appointment.cancel()`                                 | ValueError; status still COMPLETED                                                                         | Proves the guard covers every non-SCHEDULED state, and that failure leaves state unchanged.                                                       |
| TS-02   | `clinic` fixture: P1 "Alex Example" registered                           | `register_patient('P1' or ' P1 ', 'Replacement Name')` | ValueError; `find_patient('P1') is` original; name unchanged; list has one patient                         | AC-01.2 requires "without overwriting"; checking only the exception would miss an overwrite before the raise.                                     |
| TS-06   | `clinic` fixture                                                         | `find_patient('P404')`                                 | LookupError; patients list unchanged                                                                       | AC-02.2 "reports absence"; also catches a lookup that creates a placeholder.                                                                      |
| TS-10   | `clinic` fixture (P1, D1, D2)                                            | `book_appointment('A1','P1','D1',NINE)`                | `find_appointment('A1') is` result; SCHEDULED; patient/practitioner are the registered objects; time; list | AC-03.1 needs storage, not just construction; identity shows the service used the registered objects (BR-04).                                     |
| TS-15   | P2 registered; A1 booked for D1 at 09:00                                 | Book A2 for D1 at 09:00                                | ValueError; list is `[first]`; A2 absent; first still SCHEDULED                                            | AC-04.1 plus NFR-01: the rejected booking leaves no partial record.                                                                               |
| TS-18   | A1 booked for D1 at 09:00, then cancelled                                | Book A2 for D1 at 09:00                                | A2 SCHEDULED; A1 still found and CANCELLED                                                                 | Proves only SCHEDULED appointments conflict (BR-05) and history is retained. Fails if the status check is removed from the conflict rule (see J). |
| TS-19   | A1 booked                                                                | `cancel_appointment('A1')`                             | `result is booked`; CANCELLED; other fields unchanged                                                      | AC-05.1 through the real service workflow; identity proves no copy was made.                                                                      |
| TS-20   | A1 booked                                                                | `cancel_appointment('A1')`                             | `find_appointment('A1') is booked`, CANCELLED, still in list                                               | AC-05.2 retention; fails if cancellation deletes the record (see J).                                                                              |
| TS-21   | A1 booked and cancelled                                                  | Cancel A1 again                                        | ValueError; CANCELLED; still in list                                                                       | AC-05.3 rejection plus unchanged state.                                                                                                           |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour                                     | Test file/function                                                       | Result                  |
|---------|-----------------------------------------------|--------------------------------------------------------------------------|-------------------------|
| TD-01   | Valid patient kept trimmed                    | tests/test_domain.py::test_valid_patient_stores_trimmed_fields           | Passed (1)              |
| TD-02   | Blank/invalid patient ID rejected             | tests/test_domain.py::test_blank_patient_id_is_rejected                  | Passed (5 parametrised) |
| TD-03   | Blank patient name rejected                   | tests/test_domain.py::test_blank_patient_name_is_rejected                | Passed (3)              |
| TD-04   | Valid practitioner kept trimmed               | tests/test_domain.py::test_valid_practitioner_stores_trimmed_fields      | Passed (1)              |
| TD-05   | Blank practitioner ID/name/specialty rejected | tests/test_domain.py::test_blank_practitioner_fields_are_rejected        | Passed (6)              |
| TD-06   | New appointment SCHEDULED with given objects  | tests/test_domain.py::test_new_appointment_starts_scheduled              | Passed (1)              |
| TD-07   | Participants must be real objects             | tests/test_domain.py::test_appointment_requires_real_participant_objects | Passed (1)              |
| TD-08   | Invalid datetime rejected                     | tests/test_domain.py::test_invalid_appointment_time_is_rejected          | Passed (5)              |
| TD-09   | Minute-precision time accepted                | tests/test_domain.py::test_minute_precision_time_is_accepted             | Passed (1)              |
| TD-10   | Non-enum status rejected                      | tests/test_domain.py::test_non_enum_status_is_rejected                   | Passed (1)              |
| TD-11   | Identity/status read-only                     | tests/test_domain.py::test_identity_and_status_are_read_only             | Passed (1)              |
| TD-12   | Cancel changes status only                    | tests/test_domain.py::test_cancel_changes_status                         | Passed (1)              |
| TD-13   | Repeated cancel rejected                      | tests/test_domain.py::test_repeated_cancellation_is_rejected             | Passed (1)              |
| TD-14   | COMPLETED cannot be cancelled                 | tests/test_domain.py::test_completed_appointment_cannot_be_cancelled     | Passed (1)              |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour                                | Requirement / criteria          | Test file/function                                                                     | Result     |
|---------|------------------------------------------|---------------------------------|----------------------------------------------------------------------------------------|------------|
| TS-01   | Register stores and returns same object  | FR-01 / AC-01.1                 | tests/test_services.py::test_register_patient_stores_and_returns_same_object           | Passed     |
| TS-02   | Duplicate patient rejected, no overwrite | FR-01 / AC-01.2                 | tests/test_services.py::test_duplicate_patient_id_is_rejected_without_overwrite        | Passed (2) |
| TS-03   | Patient IDs case-sensitive               | FR-01 / ID contract             | tests/test_services.py::test_patient_ids_are_case_sensitive                            | Passed     |
| TS-04   | Invalid registration stores nothing      | FR-01 / validation, NFR-01      | tests/test_services.py::test_invalid_patient_registration_leaves_store_unchanged       | Passed (4) |
| TS-05   | Known patient lookup                     | FR-02 / AC-02.1                 | tests/test_services.py::test_find_known_patient_returns_stored_object                  | Passed (2) |
| TS-06   | Unknown patient lookup                   | FR-02 / AC-02.2                 | tests/test_services.py::test_find_unknown_patient_raises_lookup_error                  | Passed     |
| TS-07   | Blank patient lookup                     | FR-02 / validation              | tests/test_services.py::test_find_patient_with_blank_id_raises_value_error             | Passed (2) |
| TS-08   | Known practitioner lookup                | FR-03 supporting                | tests/test_services.py::test_find_known_practitioner_returns_stored_object             | Passed     |
| TS-09   | Unknown practitioner lookup              | FR-03 supporting                | tests/test_services.py::test_find_unknown_practitioner_raises_lookup_error             | Passed     |
| TS-10   | Booking stored and found                 | FR-04, FR-08 / AC-03.1, AC-06.1 | tests/test_services.py::test_book_appointment_stores_scheduled_appointment             | Passed     |
| TS-11   | Unknown participant blocks booking       | FR-04 / AC-03.2                 | tests/test_services.py::test_booking_unknown_participant_is_rejected                   | Passed (2) |
| TS-12   | Invalid time stores nothing              | FR-04 / datetime contract       | tests/test_services.py::test_booking_invalid_time_is_rejected_without_storing          | Passed (2) |
| TS-13   | Spaced duplicate appointment rejected    | FR-04 / BR-03                   | tests/test_services.py::test_duplicate_appointment_id_with_spaces_is_rejected          | Passed     |
| TS-14   | Unknown/blank appointment lookup         | FR-08 / lookup contract         | tests/test_services.py::test_find_unknown_appointment_raises_lookup_error              | Passed     |
| TS-15   | Exact conflict rejected                  | FR-05 / AC-04.1                 | tests/test_services.py::test_same_practitioner_same_time_conflict_is_rejected          | Passed     |
| TS-16   | Other practitioner same time allowed     | FR-05 / AC-04.2                 | tests/test_services.py::test_different_practitioner_same_time_is_allowed               | Passed     |
| TS-17   | One minute later allowed                 | FR-05 / BR-05                   | tests/test_services.py::test_same_practitioner_one_minute_later_is_allowed             | Passed     |
| TS-18   | Cancelled booking frees slot             | FR-05, FR-07 / BR-05            | tests/test_services.py::test_cancelled_booking_does_not_occupy_the_slot                | Passed     |
| TS-19   | Service cancel                           | FR-06 / AC-05.1                 | tests/test_services.py::test_cancel_appointment_changes_status_and_returns_same_object | Passed     |
| TS-20   | History retained                         | FR-07 / AC-05.2                 | tests/test_services.py::test_cancelled_appointment_remains_retrievable                 | Passed     |
| TS-21   | Repeat cancel rejected                   | FR-06 / AC-05.3                 | tests/test_services.py::test_repeated_cancellation_is_rejected_without_change          | Passed     |
| TS-22   | COMPLETED cancel rejected                | FR-06 / BR-06                   | tests/test_services.py::test_completed_appointment_cancellation_is_rejected            | Passed     |
| TS-23   | Unknown/blank cancel, no side effect     | FR-06 / cancel contract         | tests/test_services.py::test_cancel_unknown_or_blank_id_leaves_appointments_unchanged  | Passed     |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour                    | Boundary/invalid input                                           | Expected result                                | Test ID                    |
|------------------------------|------------------------------------------------------------------|------------------------------------------------|----------------------------|
| Patient ID validation        | `''`, `'   '`, `'\t\n'`, `None`, `101`                           | ValueError                                     | TD-02                      |
| Required patient name        | `''`, `'   '`, `None`                                            | ValueError                                     | TD-03                      |
| Required practitioner fields | Each of ID/name/specialty as `''` or `'   '`                     | ValueError                                     | TD-05                      |
| Appointment time             | tz-aware, 09:00:01, 09:00:00.000001, text, None                  | ValueError                                     | TD-08                      |
| Appointment time (inside)    | 23:59 with zero seconds                                          | Accepted unchanged                             | TD-09                      |
| Status type                  | `'scheduled'` text                                               | ValueError                                     | TD-10                      |
| Read-only identity           | Assign to patient_id / practitioner_id / appointment_id / status | AttributeError; values unchanged               | TD-11                      |
| Duplicate patient            | `'P1'` and `' P1 '`                                              | ValueError; original object and name kept      | TS-02                      |
| Case-sensitive ID            | `'p1'` when `'P1'` exists                                        | Accepted as a new patient                      | TS-03                      |
| Invalid registration         | Blank ID or name                                                 | ValueError; patient list unchanged             | TS-04                      |
| Lookup error types           | `'P404'` vs `''` / `'   '`                                       | LookupError vs ValueError; nothing created     | TS-06, TS-07, TS-09, TS-14 |
| Unknown participant          | P404 or D404                                                     | LookupError; no appointment stored             | TS-11                      |
| Invalid booking time         | 09:00:30, text                                                   | ValueError; no appointment stored              | TS-12                      |
| Duplicate appointment        | `' A1 '`                                                         | ValueError; original unchanged                 | TS-13                      |
| Exact conflict               | D1 at 09:00 when D1 09:00 SCHEDULED                              | ValueError; only first stored, still SCHEDULED | TS-15                      |
| Conflict edge                | D1 at 09:01                                                      | Allowed                                        | TS-17                      |
| Conflict status edge         | D1 at 09:00 when D1 09:00 is CANCELLED                           | Allowed; cancelled record kept                 | TS-18                      |
| Repeated cancel              | Cancel A1 twice                                                  | ValueError; stays CANCELLED and stored         | TD-13, TS-21               |
| COMPLETED cancel             | COMPLETED fixture                                                | ValueError; stays COMPLETED                    | TD-14, TS-22               |
| Unknown/blank cancel         | `'A404'`, `'   '`                                                | LookupError / ValueError; A1 stays SCHEDULED   | TS-23                      |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-06
<br></br>
Acceptance criterion: Repeated cancellation is rejected.
<br></br>
Behaviour to test: Cancelling an appointment that is already cancelled, raises ValueError and leaves the appointment cancelled and still stored.
<br></br>
Human-first test idea/categories:

| Idea                              | Type     | Expected result                                                   | Test  |
|-----------------------------------|----------|-------------------------------------------------------------------|-------|
| Cancel a scheduled appointment    | Valid    | Status becomes `CANCELLED`                                        | TS-19 |
| Cancel the same appointment again | Invalid  | `ValueError`; appointment remains `CANCELLED` and is still stored | TS-21 |
| Cancel a `COMPLETED` appointment  | Boundary | `ValueError`; appointment remains `COMPLETED`                     | TS-22 |
| Cancel an unknown appointment ID  | Boundary | `LookupError`                                                     | TS-23 |

Prompt and purpose: 
<br></br>"Act as a software test-design assistant.Requirement: FR-06 Cancel only a SCHEDULED appointment.Acceptance criterion: AC-05.3 Repeated cancellation is rejected.Propose pytest test candidates covering a valid case, an invalid case and meaningful boundaries. For each candidate, state exactly which required behaviour it is intended to verify. Do not invent behaviour not stated in the requirement or criterion. Use observable outcomes rather than private implementation details. Use the current SmartCare public contracts and shared SmartCareDataStore. Do not introduce SQLite, repository abstractions or unrelated features. Do not claim that a proposed test has been executed."

**Candidate 1**
- Copilot test idea/candidate: `test_cancel_scheduled_appointment_succeeds`. A SCHEDULED appointment in the store is cancelled through the public operation.
- What it claims to verify: FR-06, a SCHEDULED appointment can be cancelled, "appointment is no longer SCHEDULED when retrieved".
- Requirement trace: FR-06/AC-05.1.
- Assertion quality: Weak
- Human critique: Good idea, but it duplicates our TS-19, which asserts `status is CANCELLED` and `result is booked`.
- Decision: Reject
- Reason: Duplicate of TS-19 with a weaker assertion.
- Final test reference if accepted/modified: None
- Actual verification result: Not run as a Copilot test. Instead, TS-19 run: passed.

- **Candidate 2**
- Copilot test idea/candidate: `test_repeated_cancellation_of_same_appointment_is_rejected`. Cancel an appointment that was already cancelled.
- What it claims to verify: AC-05.3, the repeated cancellation request is rejected.
- Requirement trace: FR-06/AC-05.3.
- Assertion quality: Weak
- Human critique: The right thing to test, but it ignores the documented exception and the "leave state unchanged" contract.
- Decision: Reject
- Reason: Our TS-21 already tests this behaviour better.
- Final test reference if accepted/modified: None
- Actual verification result: Not run as a Copilot test. Instead, TS-21 run: passed.

- **Candidate 3**
- Copilot test idea/candidate: `test_second_cancellation_does_not_change_result_of_first_cancellation`. After a successful cancel, submit a second cancel and retrieve the appointment.
- What it claims to verify: A rejected second cancellation does not alter the first one, the appointment stays in its post-cancellation state.
- Requirement trace: FR-06/AC-05.3.
- Assertion quality: Good idea again. As it checks state after rejection, which candidate 2 missed.
- Human critique: Good but as a separate test it repeats candidate 2's setup and action. The state check belongs in the same test as the rejection.
- Decision: Reject
- Reason: Already covered in TS-21.
- Final test reference if accepted/modified: None
- Actual verification result: Not run as a Copilot test. Covering test TS-21 run: passed.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

**Which Copilot-generated test looked convincing but was weak?** Candidate 2, `test_repeated_cancellation_of_same_appointment_is_rejected`. It has the right name and traces straight to AC-05.3.

**Why was it weak?** Copilot's note told us not to assume a specific exception, so "rejected" would become `pytest.raises(Exception)`. That passes for any error, even the wrong one, and it never checks the appointment afterwards.

**How did you strengthen it?** Our version (TS-21) expects the documented `ValueError`, then checks if the appointment is still CANCELLED and is still saved.

**Accepted / modified / rejected test decisions and evidence:** All three candidates were rejected. Each one duplicated a human-designed test but weaker.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command            | Working directory | Code SHA                                 | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation           |
|--------------------|-------------------|------------------------------------------|--------|--------|-----------------|-------------------------------------------|---------------------------------------|
| `python -m pytest` | project/          | 9271a404479c57fd1003f27dbc537b37b58395fa | 8      | 0      | None            | None                                      | Stage 6 works cleanly with no issues. |
| `python -m pytest` | project/          | ...                                      | 74     | 0      | None            | None                                      | Stage 7 works cleanly with no issues. |

Individual test runs and changed-order independence evidence:  
- Per file: `python -m pytest tests/test_starter.py` had 8 passed, `tests/test_domain.py` had 32 passed, `tests/test_services.py` had 34 passed.
- Individual: `python -m pytest tests/test_domain.py::test_blank_patient_id_is_rejected` had 5 passed, `tests/test_services.py::test_repeated_cancellation_is_rejected_without_change` had 1 pass, `tests/test_services.py::test_cancelled_booking_does_not_occupy_the_slot` had 1 pass.
- Every new test function was also run on its own with its node ID: 37 ran, 0 failed.  

Optional tutor-led demonstration notes: ...

A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

**What does your test suite still not prove?** It does not test the date/time text parser or practitioner listing and queries.  

**Coverage if used:** Not used. 

**Which uncovered areas matter, and why does coverage percentage alone not establish correctness?** The console and query code matter most because users depend on them, and coverage would only show which lines ran.  

**Optional fixtures/parametrisation used and why, if any:** A function-scoped `clinic` fixture gives every service test a fresh shared store with P1, D1 and D2 registered, which removes repeated setup and keeps tests independent.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
Did we build the software right, and does it meet its specified requirements.

2. What question does validation answer?
Did we build the right software, and does it meet the users' needs.

3. What is a unit test?
An automated test of a small unit to check its behaviour against its contract.

4. What is a pytest fixture?
A function marked `@pytest.fixture` that gives reusable data for testing.

5. What is parametrisation in pytest?
`@pytest.mark.paramterize` runs the same test function once per listed input.

6. What is regression testing?
Re-running the whole suite after any change, to check everything works and nothing has broken.

7. What does code coverage tell us, and what does it not prove?
It shows lines or branches ran during the tests. It does not show that the results were checked.

8. What makes an assertion weak?
If it would still pass when the required behaviour is wrong.

9. What is the appropriate role of GitHub Copilot as a test assistant?
As a source for test ideas after we have designed our own.

10. What is the Stage 7 engineering rule?
Every test must trace to a real requirement and show which required behaviour it proves.

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
