# Stage 7 Testing and Verification Record

Group/tutorial: **Fri 8:30 Group 1** Members/cohorts: **Aadhya Singh, Ben Parnell, Izayah Baker, Lachlan O'Meara**
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement                         | Positive test                                                    | Negative test                                         | Key assertion                                                                                                                                             |
|-------------------------------------|------------------------------------------------------------------|-------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-01 Register patient              | Register P2 in when P1 already exists.                           | Register "P1" again, with a different name.           | Positive: `store.find_patient('P2')` is the returned patient. Negative: ValueError is raised AND `store.find_patient('P1')` is still the original object. |
| FR-05 Prevent practitioner conflict | Book D2 at 09:00 while D1 already has a scheduled booking.       | Book D1 again at exactly 09:00 while A1 is SCHEDULED. | Positive: second booking is stored and SCHEDULED. Negative: ValueError, and only the first booking is in the list.                                        |
| FR-06 Cancel appointment            | Cancel a SCHEDULED appointment with `cancel_appointment`.        | Cancel the same appointment a second time             | Positive: Positive: status is CANCELLED. Negative: ValueError and it stays CANCELLED.                                                                     |
| FR-07 Retain cancelled history      | After cancelling A1, look it up by ID and list all appointments. | Look up an appointment ID that was never booked.      | Positive: A1 is still found and listed and listed as CANCELLED. Negative: LookupError.                                                                    |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak, Why: It can never fail, so it doesn't test anything.

`assert appointment is not None`
Judgement: Weak, Why: It shows something was returned, but not that it is the right appointment. So a wrong object would still pass.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong, Why: It checks the exact required state change for AC-05.1.

`assert len(results) > 0`
Judgement:  Weak, Why: Any non-empty list passes, including the wrong records, wrong practitioner or wrong order.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong, Why: It shows the store saved that exact appoint under A1.

### Activity 3 Boundary thinking

- **Blank identifiers:** `''` and `'   '` should raise a ValueError and nothing gets saved. `' P1 '` gets trimmed to `'P1'`, so it counts as a duplicate.
<br></br>
- **Whitespace-only names/specialty:** `'   '` raises a ValueError. A name with spaces around it like ' John Smith ' is fine and gets trimmed.
  <br></br>
- **Same-time practitioner bookings:** Same practitioner at exactly 09:00 is rejected. A different practitioner at 09:00 is fine, and so is the same practitioner at 09:01, since it's only about exact times.
<br></br>
- **Cancelled appointments:** A CANCELLED 09:00 booking for D1 does not block a new 09:00 booking for D1, the cancelled record can also still be found.
<br></br>
- **Invalid status transitions:** Cancelling something already CANCELLED or COMPLETED raises a ValueError and the status does not change.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate        | What is wrong                                                              | Rewritten test intention                                                  |
|------------------|----------------------------------------------------------------------------|---------------------------------------------------------------------------|
| 1 (not None)     | Only shows an object exists, a wrong or unstored object still passes.      | Registering P2 saves it and `find_patient('P2')` returns that patient.    |
| 2 (not None)     | For booking it does not check status, participants or storage.             | Booking A1 stores a SCHEDULED appointment linked to the registered P1/D1. |
| 3 (asserts True) | Cannot fail, so it verifies nothing.                                       | Cancelling a SCHEDULED appointment changes its status to CANCELLED.       |
| 4 (SMS)          | Creates a notification feature that is not in the requirements.            | Cancelling twice raises a ValueError and it stays CANCELLED.              |
| 5 (SMS)          | Same created-requirement problem, tests behaviour SmartCare does not have. | A cancelled appointment can still be found by ID.                         |

### Tutorial exit question

**Why can 100% code coverage coexist with poor software verification?** <br></br>
Coverage only records which lines ran, not if the test actually checked the result was right. 

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

ST = supplied starter test, TD/TS = tests.

| Requirement  | Acceptance criteria                                                                                         | Test ID | Test type                       | Test name / location                                                                   | Expected behaviour                                    | Result / observed status | Supplied or student-authored |
|--------------|-------------------------------------------------------------------------------------------------------------|---------|---------------------------------|----------------------------------------------------------------------------------------|-------------------------------------------------------|--------------------------|------------------------------|
| FR-01, FR-03 | Contract: "IDs are trimmed, non-blank" and required specialty                                               | ST-01   | Domain, negative                | tests/test_starter.py::test_required_fields                                            | Blank patient ID and blank specialty raise ValueError | Passed                   | Supplied                     |
| FR-04, FR-08 | AC-03.1, AC-06.1                                                                                            | ST-02   | Service, positive               | tests/test_starter.py::test_registration_and_booking                                   | Booking stored, SCHEDULED, found by ID                | Passed                   | Supplied                     |
| FR-01        | AC-01.2                                                                                                     | ST-03   | Service, negative               | tests/test_starter.py::test_duplicate_patient_preserves_original                       | Duplicate P1 rejected, original kept                  | Passed                   | Supplied                     |
| FR-03        | Contract: "Raise ValueError for ... an existing practitioner ID"                                            | ST-04   | Service, negative               | tests/test_starter.py::test_duplicate_practitioner_preserves_original                  | Duplicate D1 rejected, original kept                  | Passed                   | Supplied                     |
| FR-04        | Contract: "Raise ValueError for ... duplicate appointment IDs"                                              | ST-05   | Service, negative               | tests/test_starter.py::test_duplicate_appointment_preserves_original                   | Duplicate A1 rejected, original kept                  | Passed                   | Supplied                     |
| FR-04        | AC-03.2                                                                                                     | ST-06   | Service + store, negative       | tests/test_starter.py::test_unregistered_participants_rejected                         | Unknown patient and lookalike patient rejected        | Passed                   | Supplied                     |
| FR-05        | AC-04.1, AC-04.2                                                                                            | ST-07   | Service, negative + positive    | tests/test_starter.py::test_conflict_rule_and_different_practitioner                   | Same slot rejected, D2 allowed                        | Passed                   | Supplied                     |
| FR-06        | AC-05.1, AC-05.3 (domain only)                                                                              | ST-08   | Domain, on a booked appointment | tests/test_starter.py::test_domain_cancellation_and_guard                              | cancel() works, second cancel rejected                | Passed                   | Supplied                     |
| FR-01        | AC-01.1 (partial, domain only)                                                                              | TD-01   | Domain, positive                | tests/test_domain.py::test_valid_patient_stores_trimmed_fields                         | ID and name kept, trimmed                             | Passed                   | Student-authored             |
| FR-01        | Contract: "IDs are trimmed, non-blank"                                                                      | TD-02   | Domain, negative/boundary       | tests/test_domain.py::test_blank_patient_id_is_rejected                                | ValueError                                            | Passed (5)               | Student-authored             |
| FR-01        | Contract: "trimmed non-blank text" (name)                                                                   | TD-03   | Domain, negative/boundary       | tests/test_domain.py::test_blank_patient_name_is_rejected                              | ValueError                                            | Passed (3)               | Student-authored             |
| FR-03        | Partial domain evidence                                                                                     | TD-04   | Domain, positive                | tests/test_domain.py::test_valid_practitioner_stores_trimmed_fields                    | ID, name, specialty kept, trimmed                     | Passed                   | Student-authored             |
| FR-03        | Contract: "trimmed non-blank text" (ID, name, specialty)                                                    | TD-05   | Domain, negative/boundary       | tests/test_domain.py::test_blank_practitioner_fields_are_rejected                      | ValueError                                            | Passed (6)               | Student-authored             |
| FR-04        | AC-03.1 (partial, initial status)                                                                           | TD-06   | Domain, positive                | tests/test_domain.py::test_new_appointment_starts_scheduled                            | SCHEDULED, keeps given objects and time               | Passed                   | Student-authored             |
| FR-04        | Contract: "IDs are trimmed, non-blank"                                                                      | TD-07   | Domain, negative/boundary       | tests/test_domain.py::test_blank_appointment_id_is_rejected                            | ValueError                                            | Passed (3)               | Student-authored             |
| FR-04        | Contract: "Invalid values ... raise ValueError" (participants)                                              | TD-08   | Domain, negative                | tests/test_domain.py::test_appointment_requires_real_participant_objects               | ValueError for IDs or swapped objects                 | Passed                   | Student-authored             |
| FR-04        | Contract: "naive, minute-precision datetime; otherwise raise ValueError"                                    | TD-09   | Domain, negative/boundary       | tests/test_domain.py::test_invalid_appointment_time_is_rejected                        | ValueError                                            | Passed (5)               | Student-authored             |
| FR-04        | Contract: "local, minute precision"                                                                         | TD-10   | Domain, boundary positive       | tests/test_domain.py::test_minute_precision_time_is_accepted                           | 23:59 accepted                                        | Passed                   | Student-authored             |
| FR-04        | Contract: "Invalid values ... raise ValueError" (status)                                                    | TD-11   | Domain, negative                | tests/test_domain.py::test_non_enum_status_is_rejected                                 | ValueError for text status                            | Passed                   | Student-authored             |
| FR-06        | Contract: "read-only identity/appointment state; changes go through domain methods"                         | TD-12   | Domain, negative                | tests/test_domain.py::test_identity_and_status_are_read_only                           | AttributeError, values unchanged                      | Passed                   | Student-authored             |
| FR-06        | AC-05.1 (domain)                                                                                            | TD-13   | Domain, positive                | tests/test_domain.py::test_cancel_changes_status                                       | CANCELLED, other fields unchanged                     | Passed                   | Student-authored             |
| FR-06        | AC-05.3 (domain)                                                                                            | TD-14   | Domain, negative                | tests/test_domain.py::test_repeated_cancellation_is_rejected                           | ValueError, stays CANCELLED                           | Passed                   | Student-authored             |
| FR-06        | Contract: "Only SCHEDULED appointments may be cancelled"                                                    | TD-15   | Domain, negative                | tests/test_domain.py::test_completed_appointment_cannot_be_cancelled                   | ValueError, stays COMPLETED                           | Passed                   | Student-authored             |
| FR-01        | AC-01.1                                                                                                     | TS-01   | Service, positive               | tests/test_services.py::test_register_patient_stores_and_returns_same_object           | Stored object is the returned object                  | Passed                   | Student-authored             |
| FR-01        | AC-01.2                                                                                                     | TS-02   | Service, negative/boundary      | tests/test_services.py::test_duplicate_patient_id_is_rejected_without_overwrite        | 'P1' and ' P1 ' rejected, original kept               | Passed (2)               | Student-authored             |
| FR-01        | Contract: "IDs are ... case-sensitive"                                                                      | TS-03   | Service, boundary positive      | tests/test_services.py::test_patient_ids_are_case_sensitive                            | 'p1' registered as a separate patient                 | Passed                   | Student-authored             |
| FR-01        | Contract: "Raise ValueError for invalid fields"                                                             | TS-04   | Service, negative               | tests/test_services.py::test_invalid_patient_registration_leaves_store_unchanged       | ValueError, store unchanged                           | Passed (4)               | Student-authored             |
| FR-02        | AC-02.1                                                                                                     | TS-05   | Service, positive               | tests/test_services.py::test_find_known_patient_returns_stored_object                  | Same object, also with ' P1 '                         | Passed (2)               | Student-authored             |
| FR-02        | AC-02.2                                                                                                     | TS-06   | Service, negative               | tests/test_services.py::test_find_unknown_patient_raises_lookup_error                  | LookupError, nothing created                          | Passed                   | Student-authored             |
| FR-02        | Contract: "Raise ValueError for a blank or invalid ID"                                                      | TS-07   | Service, negative               | tests/test_services.py::test_find_patient_with_blank_id_raises_value_error             | ValueError                                            | Passed (2)               | Student-authored             |
| FR-03        | Practitioner lookup (supporting): "Return the stored practitioner for a valid practitioner ID"              | TS-08   | Service, positive               | tests/test_services.py::test_find_known_practitioner_returns_stored_object             | Same object                                           | Passed                   | Student-authored             |
| FR-03        | Practitioner lookup (supporting): "LookupError when no practitioner is registered under it"                 | TS-09   | Service, negative               | tests/test_services.py::test_find_unknown_practitioner_raises_lookup_error             | LookupError, nothing created                          | Passed                   | Student-authored             |
| FR-03        | Practitioner lookup (supporting): "Raise ValueError for a blank or invalid ID"                              | TS-10   | Service, negative               | tests/test_services.py::test_find_practitioner_with_blank_id_raises_value_error        | ValueError                                            | Passed                   | Student-authored             |
| FR-03        | Contract: "Raise ValueError for ... an existing practitioner ID"                                            | TS-11   | Service, boundary negative      | tests/test_services.py::test_duplicate_practitioner_id_with_spaces_is_rejected         | ' D1 ' rejected, original kept                        | Passed                   | Student-authored             |
| FR-04, FR-08 | AC-03.1, AC-06.1                                                                                            | TS-12   | Service, positive               | tests/test_services.py::test_book_appointment_stores_scheduled_appointment             | Stored, SCHEDULED, registered objects, found by ID    | Passed                   | Student-authored             |
| FR-04        | AC-03.2                                                                                                     | TS-13   | Service, negative               | tests/test_services.py::test_booking_unknown_participant_is_rejected                   | LookupError, nothing stored                           | Passed (2)               | Student-authored             |
| FR-04        | Contract: "minute-precision datetime; otherwise raise ValueError"                                           | TS-14   | Service, negative               | tests/test_services.py::test_booking_invalid_time_is_rejected_without_storing          | ValueError, nothing stored                            | Passed (2)               | Student-authored             |
| FR-04        | Contract: "Raise ValueError for ... duplicate appointment IDs"                                              | TS-15   | Service, boundary negative      | tests/test_services.py::test_duplicate_appointment_id_with_spaces_is_rejected          | ' A1 ' rejected, original kept                        | Passed                   | Student-authored             |
| FR-08        | Contract: "raise LookupError when absent. Reject a blank or invalid ID with ValueError"                     | TS-16   | Service, negative               | tests/test_services.py::test_find_unknown_appointment_raises_lookup_error              | LookupError / ValueError                              | Passed                   | Student-authored             |
| FR-05        | AC-04.1                                                                                                     | TS-17   | Service, negative               | tests/test_services.py::test_same_practitioner_same_time_conflict_is_rejected          | ValueError, only first stored                         | Passed                   | Student-authored             |
| FR-05        | AC-04.2                                                                                                     | TS-18   | Service, positive               | tests/test_services.py::test_different_practitioner_same_time_is_allowed               | Both stored, SCHEDULED                                | Passed                   | Student-authored             |
| FR-05        | Contract: "No ... duration ... rules apply" (exact time only)                                               | TS-19   | Service, boundary positive      | tests/test_services.py::test_same_practitioner_one_minute_later_is_allowed             | 09:01 booking allowed                                 | Passed                   | Student-authored             |
| FR-05, FR-07 | Contract: "another SCHEDULED appointment" counts as a conflict; AC-05.2                                     | TS-20   | Service, boundary positive      | tests/test_services.py::test_cancelled_booking_does_not_occupy_the_slot                | Slot rebooked, cancelled one kept                     | Passed                   | Student-authored             |
| FR-06        | AC-05.1                                                                                                     | TS-21   | Service, positive               | tests/test_services.py::test_cancel_appointment_changes_status_and_returns_same_object | Same object, CANCELLED                                | Passed                   | Student-authored             |
| FR-07        | AC-05.2                                                                                                     | TS-22   | Service, positive               | tests/test_services.py::test_cancelled_appointment_remains_retrievable                 | Found and listed after cancel                         | Passed                   | Student-authored             |
| FR-06        | AC-05.3                                                                                                     | TS-23   | Service, negative               | tests/test_services.py::test_repeated_cancellation_is_rejected_without_change          | ValueError, still stored and CANCELLED                | Passed                   | Student-authored             |
| FR-06        | Contract: "invalid transitions (already cancelled or completed) raise ValueError and leave state unchanged" | TS-24   | Service, negative               | tests/test_services.py::test_completed_appointment_cancellation_is_rejected            | ValueError, stays COMPLETED                           | Passed                   | Student-authored             |
| FR-06        | Contract: "Unknown IDs raise LookupError; blank IDs ... raise ValueError"                                   | TS-25   | Service, negative               | tests/test_services.py::test_cancel_unknown_or_blank_id_leaves_appointments_unchanged  | Errors raised, A1 stays SCHEDULED                     | Passed                   | Student-authored             |
| FR-06        | AC-05.1                                                                                                     | TS-26   | Service, positive               | tests/test_services.py::test_cancelling_one_appointment_leaves_others_scheduled        | Only A1 is cancelled, A2 stays SCHEDULED              | Passed                   | Student-authored             |
## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criteria              | Positive/Negative/Boundary | Test intention                                       | Observable result expected             | Added evidence beyond supplied tests                                |
|---------|-------------|----------------------------------|----------------------------|------------------------------------------------------|----------------------------------------|---------------------------------------------------------------------|
| TD-01   | FR-01       | AC-01.1 (partial)                | Positive                   | Valid patient is created                             | ID and name trimmed                    | Supplied tests don't check trimming                                 |
| TD-02   | FR-01       | ID contract                      | Negative/Boundary          | Bad patient IDs are rejected                         | ValueError                             | Supplied only tries `' '`; we add `''`, tab/newline, None, a number |
| TD-03   | FR-01       | Text contract                    | Negative/Boundary          | Patient name is required                             | ValueError                             | Not covered                                                         |
| TD-04   | FR-03       | Partial                          | Positive                   | Valid practitioner is created                        | Three fields trimmed                   | Not covered                                                         |
| TD-05   | FR-03       | Text contract                    | Negative/Boundary          | Each practitioner field checked on its own           | ValueError                             | Supplied only tries an empty specialty                              |
| TD-06   | FR-04       | AC-03.1 (partial)                | Positive                   | New appointment starts SCHEDULED                     | SCHEDULED, same objects and time       | Tests the domain without the service                                |
| TD-07   | FR-04       | ID contract                      | Negative/Boundary          | Appointment ID is required                           | ValueError                             | Not covered                                                         |
| TD-08   | FR-04       | Participant contract             | Negative                   | Plain IDs or swapped objects not allowed             | ValueError                             | Not covered                                                         |
| TD-09   | FR-04       | Datetime contract                | Negative/Boundary          | Timezone, seconds, microseconds, text, None rejected | ValueError                             | Not covered                                                         |
| TD-10   | FR-04       | Datetime contract                | Boundary                   | A normal minute time is accepted                     | `date_time == edge`                    | Shows TD-09 isn't just rejecting everything                         |
| TD-11   | FR-04       | Status contract                  | Negative                   | Status has to be the enum                            | ValueError                             | Not covered                                                         |
| TD-12   | FR-06       | Read-only contract               | Negative                   | IDs and status can't be overwritten                  | AttributeError, values same            | Not covered                                                         |
| TD-13   | FR-06       | AC-05.1                          | Positive                   | cancel() only changes the status                     | CANCELLED, other fields same           | Supplied doesn't check other fields                                 |
| TD-14   | FR-06       | AC-05.3                          | Negative                   | Second cancel rejected                               | ValueError, still CANCELLED            | Kept as a required reference test                                   |
| TD-15   | FR-06       | Status guard                     | Negative                   | COMPLETED can't be cancelled                         | ValueError, still COMPLETED            | Not covered                                                         |
| TS-01   | FR-01       | AC-01.1                          | Positive                   | Register saves through the service                   | Store returns same object              | Supplied registers in a helper but never checks it                  |
| TS-02   | FR-01       | AC-01.2                          | Negative/Boundary          | Duplicate rejected, including with spaces            | ValueError, original kept              | Adds the `' P1 '` case                                              |
| TS-03   | FR-01       | ID contract                      | Boundary                   | 'p1' is a different ID to 'P1'                       | Both stored                            | Not covered                                                         |
| TS-04   | FR-01       | Validation contract              | Negative                   | Bad registration saves nothing                       | ValueError, list unchanged             | Not covered                                                         |
| TS-05   | FR-02       | AC-02.1                          | Positive                   | Find a known patient                                 | Same object                            | Stage 6 TODO, not in supplied tests                                 |
| TS-06   | FR-02       | AC-02.2                          | Negative                   | Find an unknown patient                              | LookupError                            | Stage 6 TODO                                                        |
| TS-07   | FR-02       | Lookup contract                  | Negative                   | Blank ID is ValueError, not LookupError              | ValueError                             | Checks the two errors are kept separate                             |
| TS-08   | FR-03       | Practitioner lookup              | Positive                   | Find a known practitioner                            | Same object                            | Stage 6 TODO                                                        |
| TS-09   | FR-03       | Practitioner lookup              | Negative                   | Find an unknown practitioner                         | LookupError                            | Stage 6 TODO                                                        |
| TS-10   | FR-03       | Practitioner lookup              | Negative                   | Blank practitioner ID                                | ValueError                             | Stage 6 TODO                                                        |
| TS-11   | FR-03       | Duplicate contract               | Boundary                   | `' D1 '` counts as a duplicate                       | ValueError, original kept              | Supplied only tries `'D1'`                                          |
| TS-12   | FR-04/08    | AC-03.1, AC-06.1                 | Positive                   | Booking is saved properly                            | SCHEDULED, right objects, found by ID  | Adds time and lookup checks                                         |
| TS-13   | FR-04       | AC-03.2                          | Negative                   | Unknown patient or practitioner                      | LookupError, nothing saved             | Supplied only tries an unknown patient                              |
| TS-14   | FR-04       | Datetime contract                | Negative                   | Bad time saves nothing                               | ValueError, empty list                 | Not covered                                                         |
| TS-15   | FR-04       | Duplicate contract               | Boundary                   | `' A1 '` counts as a duplicate                       | ValueError, original kept              | Adds the trimmed case                                               |
| TS-16   | FR-08       | Lookup contract                  | Negative                   | Unknown vs blank appointment ID                      | LookupError / ValueError               | Not covered                                                         |
| TS-17   | FR-05       | AC-04.1                          | Negative                   | Exact clash rejected                                 | ValueError, only first saved           | Supplied doesn't check the list after                               |
| TS-18   | FR-05       | AC-04.2                          | Positive                   | Other practitioner allowed                           | Both saved                             | Adds list check                                                     |
| TS-19   | FR-05       | Exact-time contract              | Boundary                   | One minute later isn't a clash                       | Booking saved                          | Not covered                                                         |
| TS-20   | FR-05/07    | SCHEDULED-only conflict, AC-05.2 | Boundary                   | Cancelled booking frees the slot                     | Rebook works, old one kept             | Not covered                                                         |
| TS-21   | FR-06       | AC-05.1                          | Positive                   | Cancel through the service                           | Same object, CANCELLED                 | Stage 6 TODO                                                        |
| TS-22   | FR-07       | AC-05.2                          | Positive                   | History kept after cancel                            | Found and listed                       | Stage 6 TODO                                                        |
| TS-23   | FR-06       | AC-05.3                          | Negative                   | Repeat cancel through the service                    | ValueError, still saved                | Stage 6 TODO                                                        |
| TS-24   | FR-06       | Cancel contract                  | Negative                   | COMPLETED can't be cancelled through service         | ValueError, still COMPLETED            | Not covered                                                         |
| TS-25   | FR-06       | Cancel contract                  | Negative                   | Unknown or blank ID                                  | LookupError / ValueError, A1 unchanged | Not covered                                                         |
| TS-26   | FR-06       | AC-05.1                          | Positive                   | Only the chosen appointment is cancelled             | A2 stays SCHEDULED                     | Not covered                                                         |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange                                   | Act                                             | Assert                                                                             | Why meaningful / why assertion proves criterion                                                                   |
|---------|-------------------------------------------|-------------------------------------------------|------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| TD-02   | One bad ID per parametrised case          | `Patient(bad_id, 'Alex Example')`               | `pytest.raises(ValueError)`                                                        | Uses the exact exception, so a TypeError or the ID being accepted would fail the test.                            |
| TD-13   | A new SCHEDULED appointment               | `appointment.cancel()`                          | Status is CANCELLED, ID, patient, practitioner and time unchanged                  | Shows cancel changes the status and nothing else.                                                                 |
| TS-02   | `clinic` fixture with P1 "Alex Example"   | Register 'P1' (or ' P1 ') again with a new name | ValueError, `find_patient('P1')` is the original, name the same, still one patient | AC-01.2 says no overwrite, so just checking the error would miss an overwrite that happened before it was raised. |
| TS-17   | P2 registered, A1 booked for D1 at 09:00  | Book A2 for D1 at 09:00                         | ValueError, list is `[first]`, A2 not found, first still SCHEDULED                 | Shows the rejected booking didn't leave anything behind.                                                          |
| TS-20   | A1 booked for D1 at 09:00, then cancelled | Book A2 for D1 at 09:00                         | A2 is SCHEDULED, A1 still found and CANCELLED                                      | Shows only SCHEDULED bookings cause a clash, and the cancelled one isn't deleted.                                 |
| TS-23   | A1 booked and cancelled                   | Cancel A1 again                                 | ValueError, still CANCELLED and still in the list                                  | Checks the rejection and that nothing changed.                                                                    |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour                                     | Test file/function                                                       | Result     |
|---------|-----------------------------------------------|--------------------------------------------------------------------------|------------|
| TD-01   | Valid patient kept trimmed                    | tests/test_domain.py::test_valid_patient_stores_trimmed_fields           | Passed     |
| TD-02   | Blank/invalid patient ID rejected             | tests/test_domain.py::test_blank_patient_id_is_rejected                  | Passed (5) |
| TD-03   | Blank patient name rejected                   | tests/test_domain.py::test_blank_patient_name_is_rejected                | Passed (3) |
| TD-04   | Valid practitioner kept trimmed               | tests/test_domain.py::test_valid_practitioner_stores_trimmed_fields      | Passed     |
| TD-05   | Blank practitioner ID/name/specialty rejected | tests/test_domain.py::test_blank_practitioner_fields_are_rejected        | Passed (6) |
| TD-06   | New appointment is SCHEDULED                  | tests/test_domain.py::test_new_appointment_starts_scheduled              | Passed     |
| TD-07   | Blank appointment ID rejected                 | tests/test_domain.py::test_blank_appointment_id_is_rejected              | Passed (3) |
| TD-08   | Needs real Patient/Practitioner objects       | tests/test_domain.py::test_appointment_requires_real_participant_objects | Passed     |
| TD-09   | Invalid time rejected                         | tests/test_domain.py::test_invalid_appointment_time_is_rejected          | Passed (5) |
| TD-10   | Minute time accepted                          | tests/test_domain.py::test_minute_precision_time_is_accepted             | Passed     |
| TD-11   | Text status rejected                          | tests/test_domain.py::test_non_enum_status_is_rejected                   | Passed     |
| TD-12   | IDs and status are read-only                  | tests/test_domain.py::test_identity_and_status_are_read_only             | Passed     |
| TD-13   | Cancel changes only status                    | tests/test_domain.py::test_cancel_changes_status                         | Passed     |
| TD-14   | Repeated cancel rejected                      | tests/test_domain.py::test_repeated_cancellation_is_rejected             | Passed     |
| TD-15   | COMPLETED can't be cancelled                  | tests/test_domain.py::test_completed_appointment_cannot_be_cancelled     | Passed     |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour                              | Requirement / criteria                 | Test file/function                                                                     | Result     |
|---------|----------------------------------------|----------------------------------------|----------------------------------------------------------------------------------------|------------|
| TS-01   | Register saves the patient             | FR-01 / AC-01.1                        | tests/test_services.py::test_register_patient_stores_and_returns_same_object           | Passed     |
| TS-02   | Duplicate patient rejected             | FR-01 / AC-01.2                        | tests/test_services.py::test_duplicate_patient_id_is_rejected_without_overwrite        | Passed (2) |
| TS-03   | Patient IDs case-sensitive             | FR-01 / ID contract                    | tests/test_services.py::test_patient_ids_are_case_sensitive                            | Passed     |
| TS-04   | Bad registration saves nothing         | FR-01 / validation contract            | tests/test_services.py::test_invalid_patient_registration_leaves_store_unchanged       | Passed (4) |
| TS-05   | Find known patient                     | FR-02 / AC-02.1                        | tests/test_services.py::test_find_known_patient_returns_stored_object                  | Passed (2) |
| TS-06   | Find unknown patient                   | FR-02 / AC-02.2                        | tests/test_services.py::test_find_unknown_patient_raises_lookup_error                  | Passed     |
| TS-07   | Find blank patient ID                  | FR-02 / lookup contract                | tests/test_services.py::test_find_patient_with_blank_id_raises_value_error             | Passed (2) |
| TS-08   | Find known practitioner                | FR-03 / practitioner lookup            | tests/test_services.py::test_find_known_practitioner_returns_stored_object             | Passed     |
| TS-09   | Find unknown practitioner              | FR-03 / practitioner lookup            | tests/test_services.py::test_find_unknown_practitioner_raises_lookup_error             | Passed     |
| TS-10   | Find blank practitioner ID             | FR-03 / practitioner lookup            | tests/test_services.py::test_find_practitioner_with_blank_id_raises_value_error        | Passed     |
| TS-11   | Spaced duplicate practitioner rejected | FR-03 / duplicate contract             | tests/test_services.py::test_duplicate_practitioner_id_with_spaces_is_rejected         | Passed     |
| TS-12   | Booking saved and found                | FR-04, FR-08 / AC-03.1, AC-06.1        | tests/test_services.py::test_book_appointment_stores_scheduled_appointment             | Passed     |
| TS-13   | Unknown participant rejected           | FR-04 / AC-03.2                        | tests/test_services.py::test_booking_unknown_participant_is_rejected                   | Passed (2) |
| TS-14   | Bad time saves nothing                 | FR-04 / datetime contract              | tests/test_services.py::test_booking_invalid_time_is_rejected_without_storing          | Passed (2) |
| TS-15   | Spaced duplicate appointment rejected  | FR-04 / duplicate contract             | tests/test_services.py::test_duplicate_appointment_id_with_spaces_is_rejected          | Passed     |
| TS-16   | Unknown/blank appointment lookup       | FR-08 / lookup contract                | tests/test_services.py::test_find_unknown_appointment_raises_lookup_error              | Passed     |
| TS-17   | Exact clash rejected                   | FR-05 / AC-04.1                        | tests/test_services.py::test_same_practitioner_same_time_conflict_is_rejected          | Passed     |
| TS-18   | Other practitioner allowed             | FR-05 / AC-04.2                        | tests/test_services.py::test_different_practitioner_same_time_is_allowed               | Passed     |
| TS-19   | One minute later allowed               | FR-05 / exact-time contract            | tests/test_services.py::test_same_practitioner_one_minute_later_is_allowed             | Passed     |
| TS-20   | Cancelled booking frees slot           | FR-05, FR-07 / SCHEDULED-only conflict | tests/test_services.py::test_cancelled_booking_does_not_occupy_the_slot                | Passed     |
| TS-21   | Cancel through service                 | FR-06 / AC-05.1                        | tests/test_services.py::test_cancel_appointment_changes_status_and_returns_same_object | Passed     |
| TS-22   | Cancelled history kept                 | FR-07 / AC-05.2                        | tests/test_services.py::test_cancelled_appointment_remains_retrievable                 | Passed     |
| TS-23   | Repeat cancel rejected                 | FR-06 / AC-05.3                        | tests/test_services.py::test_repeated_cancellation_is_rejected_without_change          | Passed     |
| TS-24   | COMPLETED cancel rejected              | FR-06 / cancel contract                | tests/test_services.py::test_completed_appointment_cancellation_is_rejected            | Passed     |
| TS-25   | Unknown/blank cancel changes nothing   | FR-06 / cancel contract                | tests/test_services.py::test_cancel_unknown_or_blank_id_leaves_appointments_unchanged  | Passed     |
| TS-26   | Cancelling one leaves others alone     | FR-06 / AC-05.1                        | tests/test_services.py::test_cancelling_one_appointment_leaves_others_scheduled        | Passed     |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour                     | Boundary/invalid input                                         | Expected result                              | Test ID                           |
|-------------------------------|----------------------------------------------------------------|----------------------------------------------|-----------------------------------|
| Patient ID                    | `''`, `'   '`, `'\t\n'`, `None`, `101`                         | ValueError                                   | TD-02                             |
| Patient name                  | `''`, `'   '`, `None`                                          | ValueError                                   | TD-03                             |
| Practitioner fields           | Each of ID/name/specialty as `''` or `'   '`                   | ValueError                                   | TD-05                             |
| Appointment ID                | `''`, `'   '`, `None`                                          | ValueError                                   | TD-07                             |
| Appointment time              | timezone-aware, 09:00:01, 09:00:00.000001, text, None          | ValueError                                   | TD-09                             |
| Appointment time (valid edge) | 23:59 with zero seconds                                        | Accepted                                     | TD-10                             |
| Status                        | `'scheduled'` as text                                          | ValueError                                   | TD-11                             |
| Read-only fields              | Setting patient_id / practitioner_id / appointment_id / status | AttributeError, values unchanged             | TD-12                             |
| Duplicate patient             | `'P1'` and `' P1 '`                                            | ValueError, original kept                    | TS-02                             |
| Case-sensitive ID             | `'p1'` when `'P1'` exists                                      | Accepted as a new patient                    | TS-03                             |
| Bad registration              | Blank ID or name                                               | ValueError, patient list unchanged           | TS-04                             |
| Lookup errors                 | `'P404'` / `'D404'` / `'A404'` vs `''` / `'   '`               | LookupError vs ValueError, nothing created   | TS-06, TS-07, TS-09, TS-10, TS-16 |
| Duplicate practitioner        | `' D1 '`                                                       | ValueError, original kept                    | TS-11                             |
| Unknown participant           | P404 or D404                                                   | LookupError, nothing stored                  | TS-13                             |
| Bad booking time              | 09:00:30, text                                                 | ValueError, nothing stored                   | TS-14                             |
| Duplicate appointment         | `' A1 '`                                                       | ValueError, original kept                    | TS-15                             |
| Exact clash                   | D1 at 09:00 when D1 09:00 is SCHEDULED                         | ValueError, only first stored                | TS-17                             |
| Clash edge                    | D1 at 09:01                                                    | Allowed                                      | TS-19                             |
| Cancelled slot                | D1 at 09:00 when D1 09:00 is CANCELLED                         | Allowed, cancelled one kept                  | TS-20                             |
| Repeated cancel               | Cancel A1 twice                                                | ValueError, stays CANCELLED and stored       | TD-14, TS-23                      |
| COMPLETED cancel              | COMPLETED appointment                                          | ValueError, stays COMPLETED                  | TD-15, TS-24                      |
| Unknown/blank cancel          | `'A404'`, `'   '`                                              | LookupError / ValueError, A1 stays SCHEDULED | TS-25                             |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-06 Cancel appointment
<br></br>
Acceptance criterion: AC-05.3 Repeated cancellation is rejected.
<br></br>
Behaviour to test: Cancelling an appointment that's already cancelled raises ValueError, and the appointment stays cancelled and still saved.
<br></br>
Human-first test idea/categories:

| Idea                              | Type     | Expected result                             | Test  |
|-----------------------------------|----------|---------------------------------------------|-------|
| Cancel a scheduled appointment    | Valid    | Status becomes CANCELLED                    | TS-21 |
| Cancel the same appointment again | Invalid  | ValueError, stays CANCELLED and still saved | TS-23 |
| Cancel a COMPLETED appointment    | Boundary | ValueError, stays COMPLETED                 | TS-24 |
| Cancel an unknown appointment ID  | Boundary | LookupError                                 | TS-25 |

Prompt and purpose:
<br></br>"Act as a software test-design assistant. Requirement: FR-06 Cancel only a SCHEDULED appointment. Acceptance criterion: AC-05.3 Repeated cancellation is rejected. Propose pytest test candidates covering a valid case, an invalid case and meaningful boundaries. For each candidate, state exactly which required behaviour it is intended to verify. Do not invent behaviour not stated in the requirement or criterion. Use observable outcomes rather than private implementation details. Use the current SmartCare public contracts and shared SmartCareDataStore. Do not introduce SQLite, repository abstractions or unrelated features. Do not claim that a proposed test has been executed."

**Candidate 1**
- Copilot test idea/candidate: `test_cancel_scheduled_appointment_succeeds`. Cancel a SCHEDULED appointment in the store.
- What it claims to verify: A SCHEDULED appointment can be cancelled, it is "no longer SCHEDULED when retrieved".
- Requirement trace: FR-06 / AC-05.1
- Assertion quality: Weak, it only checks the status isn't SCHEDULED, not that it's CANCELLED.
- Human critique: Good idea, but it's the same as our TS-21, which checks the status is CANCELLED and the same object comes back.
- Decision: Reject
- Reason: Duplicate of TS-21 with a weaker assertion.
- Final test reference if accepted/modified: None
- Actual verification result: Not run as a Copilot test. TS-21 was run instead: passed.

**Candidate 2**
- Copilot test idea/candidate: `test_repeated_cancellation_of_same_appointment_is_rejected`. Cancel an appointment that was already cancelled.
- What it claims to verify: AC-05.3, the second cancel is rejected.
- Requirement trace: FR-06 / AC-05.3
- Assertion quality: Weak
- Human critique: Right thing to test, but it doesn't expect ValueError and doesn't check the appointment afterwards.
- Decision: Reject
- Reason: Our TS-23 already tests this better.
- Final test reference if accepted/modified: None
- Actual verification result: Not run as a Copilot test. TS-23 was run instead: passed.

**Candidate 3**
- Copilot test idea/candidate: `test_second_cancellation_does_not_change_result_of_first_cancellation`. Cancel, cancel again, then look the appointment up.
- What it claims to verify: The rejected second cancel doesn't change anything.
- Requirement trace: FR-06 / AC-05.3
- Assertion quality: OK, it checks the state after the rejection, which candidate 2 missed.
- Human critique: As its own test it repeats candidate 2's setup. The state check should be in the same test as the rejection.
- Decision: Reject
- Reason: Already covered by TS-23.
- Final test reference if accepted/modified: None
- Actual verification result: Not run as a Copilot test. TS-23 was run instead: passed.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

**Which Copilot-generated test looked convincing but was weak?** Candidate 2, `test_repeated_cancellation_of_same_appointment_is_rejected`. It has the right name and traces back to AC-05.3.

**Why was it weak?** Copilot's note told us not to assume a specific exception, so "rejected" would become `pytest.raises(Exception)`. That passes for any error, even the wrong one, and it never checks the appointment afterwards.

**How did you strengthen it?** Our version (TS-23) expects the documented `ValueError`, then checks if the appointment is still CANCELLED and is still saved.

**Accepted / modified / rejected test decisions and evidence:** All three candidates were rejected. Each one duplicated a human-designed test but weaker.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command            | Working directory | Code SHA                                 | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation                                 |
|--------------------|-------------------|------------------------------------------|--------|--------|-----------------|-------------------------------------------|-------------------------------------------------------------|
| `python -m pytest` | project/          | 9271a404479c57fd1003f27dbc537b37b58395fa | 8      | 0      | None            | None                                      | Stage 6 baseline before our tests, all supplied tests pass. |
| `python -m pytest` | project/          | b8029b0adb82d8beae7cb5de424037445a2cf552 | 74     | 0      | None            | None                                      | Stage 7, all 8 starter tests and our new tests pass.        |

Individual test runs and changed-order independence evidence:
- Per file: `python -m pytest tests/test_starter.py` 8 passed, `tests/test_domain.py` 32 passed, `tests/test_services.py` 34 passed.
- Individual: each of our 41 new test functions (15 in test_domain.py, 26 in test_services.py) was run on its own with its ID, e.g. `python -m pytest tests/test_services.py::test_cancelled_booking_does_not_occupy_the_slot`. All passed.
- Changed order: we ran all the IDs from test_domain.py and test_services.py in reverse order in one command, 66 passed. So the tests don't depend on each other. 

Optional tutor-led demonstration notes: ...

A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: No tests failed in stage 7, so there was nothing to diagnose or change.

## K What the Suite Still Does Not Prove

**What does your test suite still not prove?** It does not test the date/time text parser or practitioner listing and queries.  

**Coverage if used:** Not used. 

**Which uncovered areas matter, and why does coverage percentage alone not establish correctness?** The console and query code matter most because users depend on them, and coverage would only show which lines ran.  

**Optional fixtures/parametrisation used and why, if any:** A function-scoped `clinic` fixture gives every service test a fresh shared store with P1, D1 and D2 registered, which removes repeated setup and keeps tests independent.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task                                       | Branch                    | PR   | Reviewer      | Key feedback  | Outcome                                                                                                                                                                                           |
|--------------------------------------------------|---------------------------|------|---------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Stage 7 domain and service tests and this record | main (no separate branch) | None | None recorded | None recorded | Committed straight to main: [b8029b0](https://github.com/BenP64/st1-assignment-3/commit/b8029b0adb82d8beae7cb5de424037445a2cf552) "Stage 7 upload - evidence mostly complete, test code included" |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member          | Actual contribution                                                                                     | Evidence link                                                                                         |
|-----------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Ben Parnell     | Wrote the Stage 7 tests in test_domain.py and test_services.py, ran the suite and filled in this record | [b8029b0](https://github.com/BenP64/st1-assignment-3/commit/b8029b0adb82d8beae7cb5de424037445a2cf552) |

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

Tested Stage 7 main SHA: b8029b0adb82d8beae7cb5de424037445a2cf552
Full-suite result: `python -m pytest` from project/, 74 passed, 0 failed.
Unresolved defects and effect on baseline: None. No product or test defects were found in Stage 7.
Clean working tree and integration evidence: The tests and record were committed and pushed to main as b8029b0. This record was updated afterwards as an evidence-only change, no code was changed.
Stage 8 handover status: Ready. Stage 8 started from this commit (2d4b8df "Prepare stage 08 Debug" has b8029b0 as its parent). No Stage 8 work was done in Stage 7.
All tutorial/formative responses and traceability/Copilot decisions complete: Yes, A to K and N are done. L and M still need the group to check.
