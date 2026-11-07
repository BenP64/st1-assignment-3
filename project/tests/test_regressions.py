"""Stage 8 regression tests for the two prepared defects.

F8-01: a practitioner must not be double-booked at the same time
       (FR-05 / AC-04.1), while a different practitioner at that time is
       still allowed (AC-04.2).
F8-02: a cancelled appointment must stay in the store and remain findable
       as the same object with CANCELLED status (FR-06/07, FR-08, BR-07,
       AC-05.2).

Each test should FAIL on the prepared faulty branch and PASS after repair.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


WHEN = datetime(2026, 10, 1, 9, 0)


@pytest.fixture
def setup():
    """Fresh store with patients P1, P2 and practitioners D1, D2."""
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Sam Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Morgan Example', 'General')
    return store, AppointmentService(store)


def test_f8_01_same_practitioner_same_time_rejected_without_change(setup):
    """F8-01: second booking for D1 at the same time is rejected and
    nothing in the store changes; D2 at that time is still allowed.
    """
    store, appointments = setup
    first = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    with pytest.raises(ValueError):
        appointments.book_appointment('A2', 'P2', 'D1', WHEN)

    # The rejected booking left the store unchanged.
    assert store.find_appointment('A2') is None
    assert store.list_appointments() == [first]
    assert first.status is AppointmentStatus.SCHEDULED

    # A different practitioner at the same time is not a conflict.
    other = appointments.book_appointment('A3', 'P2', 'D2', WHEN)
    assert store.find_appointment('A3') is other


def test_f8_02_cancelled_appointment_is_retained_and_found(setup):
    """F8-02: after cancellation the same object is still stored, listed
    and found, with CANCELLED status; a repeat cancel is rejected.
    """
    store, appointments = setup
    booked = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    cancelled = appointments.cancel_appointment('A1')

    assert cancelled is booked
    assert booked.status is AppointmentStatus.CANCELLED
    # Store lookup returns the object (not None) ...
    assert store.find_appointment('A1') is booked
    # ... service lookup returns it (no LookupError) ...
    assert appointments.find_appointment('A1') is booked
    # ... and it is still listed.
    assert booked in store.list_appointments()

    # Cancelling again is an invalid transition: ValueError, no change.
    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')
    assert booked.status is AppointmentStatus.CANCELLED
    assert store.list_appointments() == [booked]