
from datetime import datetime

import pytest
from smartcare.console import run_menu
from smartcare.data_store import SmartCareDataStore
from smartcare.services import (
    PatientService,
    PractitionerService,
    AppointmentService,
)
from smartcare.domain import AppointmentStatus


def test_complete_appointment_workflow():
    # All services share one session store.
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    # Register participants.
    patients.register_patient("P1", "Alex")
    practitioners.register_practitioner("D1", "Taylor", "General")
    practitioners.register_practitioner("D2", "Jordan", "Cardiology")

    date_time = datetime(2026, 10, 1, 9, 0)

    # Book the first appointment.
    first = appointments.book_appointment(
        "A1", "P1", "D1", date_time
    )

    assert first.status is AppointmentStatus.SCHEDULED

    # Reject a conflicting appointment without changing the store.
    before = store.list_appointments()

    with pytest.raises(ValueError):
        appointments.book_appointment(
            "A-CONFLICT", "P1", "D1", date_time
        )

    assert store.list_appointments() == before

    with pytest.raises(LookupError):
        appointments.find_appointment("A-CONFLICT")

    # Another practitioner can be booked at the same time.
    second = appointments.book_appointment(
        "A2", "P1", "D2", date_time
    )

    assert second.status is AppointmentStatus.SCHEDULED

    # Cancel A1 but retain the original object.
    cancelled = appointments.cancel_appointment("A1")

    assert cancelled is first
    assert first.status is AppointmentStatus.CANCELLED
    assert appointments.find_appointment("A1") is first

    # All-status listing includes cancelled history.
    assert appointments.list_practitioner_appointments(
        "D1"
    ) == [first]

    # Scheduled-only listing excludes cancelled history.
    assert appointments.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    ) == []

    # The cancelled appointment's time slot is available again.
    third = appointments.book_appointment(
        "A3", "P1", "D1", date_time
    )

    assert third.status is AppointmentStatus.SCHEDULED

    # Both the retained history and new booking are visible.
    result = appointments.list_practitioner_appointments("D1")

    assert result == [first, third]
    assert result[0] is first
    assert result[1] is third

def test_console_error_recovery(monkeypatch, capsys):
    # Simulate user inputs for one complete console session.
    user_inputs = iter([
        "1", "P1", "Alex",
        "3", "D1", "Taylor", "General",
        "5", "A1", "P1", "D1", "2026-10-01 09:00",

        # Invalid menu choice.
        "99",

        # Duplicate patient registration.
        "1", "P1", "Another Name",

        # Invalid blank patient ID.
        "2", " ",

        # Booking with an unknown patient.
        "5", "A2", "UNKNOWN", "D1", "2026-10-01 10:00",

        # Malformed and impossible dates.
        "5", "BAD", "P1", "D1", "not a date",
        "5", "BAD", "P1", "D1", "2026-02-30 09:00",

        # Unknown appointment.
        "7", "UNKNOWN",

        # Invalid status filter.
        "8", "D1", "pending",

        # First cancellation succeeds, second must fail.
        "6", "A1",
        "6", "A1",

        # Cancelled appointment remains retrievable.
        "7", "A1",
        "8", "D1", "",

        # Scheduled-only list excludes cancelled A1.
        "8", "D1", "scheduled",

        # Previously rejected ID can now be used.
        "5", "BAD", "P1", "D1", "2026-10-01 10:00",

        "0",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(user_inputs)
    )

    run_menu()

    output = capsys.readouterr().out

    # The program recovered from invalid inputs.
    assert "Invalid menu choice" in output
    assert output.count("Error:") >= 8

    # Cancellation works and retains history.
    assert "Cancelled: A1:" in output
    assert "cancelled" in output.lower()

    # Cancelled appointment is excluded from scheduled listing.
    assert "No matching appointments." in output

    # Failed bookings did not reserve the appointment ID.
    assert "Booked: BAD:" in output

    # Console exits normally.
    assert "Goodbye" in output


def test_console_lookup_and_listing_order(monkeypatch, capsys):
    user_inputs = iter([
        "1", "P1", "Alex",
        "3", "D1", "Taylor", "General",
        "2", "P1",
        "4", "D1",
        "5", "A2", "P1", "D1", "2026-10-01 11:00",
        "5", "A1", "P1", "D1", "2026-10-01 09:00",
        "8", "D1", "",
        "0",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(user_inputs)
    )

    run_menu()
    output = capsys.readouterr().out

    # Patient and practitioner lookup succeed.
    assert "Patient: P1 - Alex" in output
    assert "Practitioner: D1 - Taylor (General)" in output

    # Listing is ordered by appointment date/time,
    # not by the order appointments were created.
    listing_lines = [
        line.strip()
        for line in output.splitlines()
        if line.startswith(("A1: ", "A2: "))
    ]

    assert len(listing_lines) == 2
    assert listing_lines[0].startswith("A1:")
    assert listing_lines[1].startswith("A2:")

    assert "Goodbye" in output
