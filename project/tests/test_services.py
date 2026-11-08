"""Tests for the patient, practitioner and appointment services working together.
"""

from dataclasses import dataclass
from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


NINE = datetime(2026, 10, 1, 9, 0)
NINE_ONE = datetime(2026, 10, 1, 9, 1)


@dataclass
class Clinic:
    """Holds one store, its three services and the people registered in it."""

    store: SmartCareDataStore
    patients: PatientService
    practitioners: PractitionerService
    appointments: AppointmentService
    patient: Patient
    doctor: Practitioner
    other_doctor: Practitioner


@pytest.fixture
def clinic() -> Clinic:
    """Set up a fresh store with patient P1 and practitioners D1 and D2."""
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    return Clinic(
        store=store,
        patients=patients,
        practitioners=practitioners,
        appointments=AppointmentService(store),
        patient=patients.register_patient('P1', 'Alex Example'),
        doctor=practitioners.register_practitioner(
            'D1', 'Taylor Example', 'General',
        ),
        other_doctor=practitioners.register_practitioner(
            'D2', 'Morgan Example', 'General',
        ),
    )


# --- FR-01 patient registration ----

def test_register_patient_stores_and_returns_same_object(
    clinic: Clinic,
) -> None:
    """TS-01: Registering a new patient stores it, and we get back the stored
    patient.
    """
    patient = clinic.patients.register_patient('P2', 'Jordan Example')

    assert clinic.store.find_patient('P2') is patient
    assert patient.name == 'Jordan Example'
    assert clinic.store.list_patients() == [clinic.patient, patient]


@pytest.mark.parametrize('duplicate_id', ['P1', '  P1  '])
def test_duplicate_patient_id_is_rejected_without_overwrite(
    clinic: Clinic,
    duplicate_id: str,
) -> None:
    """TS-02: Registering P1 again (even with spaces) fails and the original
    patient is kept.
    """
    with pytest.raises(ValueError):
        clinic.patients.register_patient(duplicate_id, 'Replacement Name')

    assert clinic.store.find_patient('P1') is clinic.patient
    assert clinic.patient.name == 'Alex Example'
    assert clinic.store.list_patients() == [clinic.patient]


def test_patient_ids_are_case_sensitive(clinic: Clinic) -> None:
    """TS-03: 'p1' and 'P1' are different patients because IDs are
    case-sensitive.
    """
    lower = clinic.patients.register_patient('p1', 'Casey Example')

    assert clinic.store.find_patient('p1') is lower
    assert clinic.store.find_patient('P1') is clinic.patient


@pytest.mark.parametrize(
    ('patient_id', 'name'),
    [('', 'Jordan Example'), ('   ', 'Jordan Example'),
     ('P2', ''), ('P2', '   ')],
)
def test_invalid_patient_registration_leaves_store_unchanged(
    clinic: Clinic,
    patient_id: str,
    name: str,
) -> None:
    """TS-04: A blank ID or name is rejected and nothing gets stored."""
    with pytest.raises(ValueError):
        clinic.patients.register_patient(patient_id, name)

    assert clinic.store.list_patients() == [clinic.patient]


# --- FR-02 patient lookup ---

@pytest.mark.parametrize('lookup_id', ['P1', ' P1 '])
def test_find_known_patient_returns_stored_object(
    clinic: Clinic,
    lookup_id: str,
) -> None:
    """TS-05: Looking up P1 returns the exact patient that was registered."""
    assert clinic.patients.find_patient(lookup_id) is clinic.patient


def test_find_unknown_patient_raises_lookup_error(clinic: Clinic) -> None:
    """TS-06: Looking up a patient that doesn't exist raises LookupError."""
    with pytest.raises(LookupError):
        clinic.patients.find_patient('P404')

    assert clinic.store.list_patients() == [clinic.patient]


@pytest.mark.parametrize('blank_id', ['', '   '])
def test_find_patient_with_blank_id_raises_value_error(
    clinic: Clinic,
    blank_id: str,
) -> None:
    """TS-07: Looking up a blank ID raises ValueError, not LookupError."""
    with pytest.raises(ValueError):
        clinic.patients.find_patient(blank_id)


# --- FR-03 practitioner registration and supporting lookup ---

def test_find_known_practitioner_returns_stored_object(
    clinic: Clinic,
) -> None:
    """TS-08: Looking up D1 returns the exact practitioner that was registered."""
    found = clinic.practitioners.find_practitioner(' D1 ')

    assert found is clinic.doctor
    assert found.specialty == 'General'


def test_find_unknown_practitioner_raises_lookup_error(
    clinic: Clinic,
) -> None:
    """TS-09: Looking up a practitioner that doesn't exist raises LookupError."""
    with pytest.raises(LookupError):
        clinic.practitioners.find_practitioner('D404')

    assert clinic.store.list_practitioners() == [
        clinic.doctor, clinic.other_doctor,
    ]


def test_find_practitioner_with_blank_id_raises_value_error(
    clinic: Clinic,
) -> None:
    """TS-10: Looking up a blank practitioner ID raises ValueError."""
    with pytest.raises(ValueError):
        clinic.practitioners.find_practitioner('   ')


def test_duplicate_practitioner_id_with_spaces_is_rejected(
    clinic: Clinic,
) -> None:
    """TS-11: ' D1 ' counts as D1, so it's rejected and the original is kept."""
    with pytest.raises(ValueError):
        clinic.practitioners.register_practitioner(
            ' D1 ', 'Replacement', 'Other',
        )

    assert clinic.store.find_practitioner('D1') is clinic.doctor
    assert clinic.doctor.name == 'Taylor Example'
    assert clinic.doctor.specialty == 'General'


# --- FR-04 / FR-08 booking and appointment lookup ---

def test_book_appointment_stores_scheduled_appointment(
    clinic: Clinic,
) -> None:
    """TS-12: Booking stores a SCHEDULED appointment with the registered
    patient and practitioner, and we can find it by ID.
    """
    appointment = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)

    assert clinic.appointments.find_appointment('A1') is appointment
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.patient is clinic.patient
    assert appointment.practitioner is clinic.doctor
    assert appointment.date_time == NINE
    assert clinic.store.list_appointments() == [appointment]


@pytest.mark.parametrize(
    ('patient_id', 'practitioner_id'),
    [('P404', 'D1'), ('P1', 'D404')],
    ids=['unknown-patient', 'unknown-practitioner'],
)
def test_booking_unknown_participant_is_rejected(
    clinic: Clinic,
    patient_id: str,
    practitioner_id: str,
) -> None:
    """TS-13: Booking with an unknown patient or practitioner fails and nothing
    is stored.
    """
    with pytest.raises(LookupError):
        clinic.appointments.book_appointment(
            'A1', patient_id, practitioner_id, NINE,
        )

    assert clinic.store.list_appointments() == []
    assert clinic.store.find_appointment('A1') is None


@pytest.mark.parametrize(
    'bad_time',
    [datetime(2026, 10, 1, 9, 0, 30), '2026-10-01 09:00'],
    ids=['nonzero-second', 'text'],
)
def test_booking_invalid_time_is_rejected_without_storing(
    clinic: Clinic,
    bad_time: object,
) -> None:
    """TS-14: Booking with an invalid time fails and nothing is stored."""
    with pytest.raises(ValueError):
        clinic.appointments.book_appointment(
            'A1', 'P1', 'D1', bad_time,
        )

    assert clinic.store.list_appointments() == []


def test_duplicate_appointment_id_with_spaces_is_rejected(
    clinic: Clinic,
) -> None:
    """TS-15: ' A1 ' counts as A1, so the second booking is rejected."""
    original = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)

    with pytest.raises(ValueError):
        clinic.appointments.book_appointment(' A1 ', 'P1', 'D2', NINE_ONE)

    assert clinic.store.list_appointments() == [original]
    assert original.practitioner is clinic.doctor
    assert original.date_time == NINE


def test_find_unknown_appointment_raises_lookup_error(
    clinic: Clinic,
) -> None:
    """TS-16: An unknown appointment ID raises LookupError; a blank one raises
    ValueError.
    """
    with pytest.raises(LookupError):
        clinic.appointments.find_appointment('A404')
    with pytest.raises(ValueError):
        clinic.appointments.find_appointment('  ')


# --- FR-05 practitioner conflict ---

def test_same_practitioner_same_time_conflict_is_rejected(
    clinic: Clinic,
) -> None:
    """TS-17: The same practitioner can't be booked twice at the same time."""
    clinic.patients.register_patient('P2', 'Jordan Example')
    first = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)

    with pytest.raises(ValueError):
        clinic.appointments.book_appointment('A2', 'P2', 'D1', NINE)

    assert clinic.store.list_appointments() == [first]
    assert clinic.store.find_appointment('A2') is None
    assert first.status is AppointmentStatus.SCHEDULED


def test_different_practitioner_same_time_is_allowed(
    clinic: Clinic,
) -> None:
    """TS-18: A different practitioner can be booked at the same time."""
    first = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)

    second = clinic.appointments.book_appointment('A2', 'P1', 'D2', NINE)

    assert second.practitioner is clinic.other_doctor
    assert second.status is AppointmentStatus.SCHEDULED
    assert clinic.store.list_appointments() == [first, second]


def test_same_practitioner_one_minute_later_is_allowed(
    clinic: Clinic,
) -> None:
    """TS-19: One minute later isn't a clash, since only the exact same time
    counts.
    """
    clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)

    later = clinic.appointments.book_appointment('A2', 'P1', 'D1', NINE_ONE)

    assert clinic.appointments.find_appointment('A2') is later
    assert len(clinic.store.list_appointments()) == 2


def test_cancelled_booking_does_not_occupy_the_slot(
    clinic: Clinic,
) -> None:
    """TS-20: Once a booking is cancelled, that time slot can be booked again."""
    cancelled = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)
    clinic.appointments.cancel_appointment('A1')

    rebooked = clinic.appointments.book_appointment('A2', 'P1', 'D1', NINE)

    assert rebooked.status is AppointmentStatus.SCHEDULED
    assert clinic.appointments.find_appointment('A1') is cancelled
    assert cancelled.status is AppointmentStatus.CANCELLED


# --- FR-06 / FR-07 cancellation and retained history ---

def test_cancel_appointment_changes_status_and_returns_same_object(
    clinic: Clinic,
) -> None:
    """TS-21: Cancelling returns the same appointment, now CANCELLED."""
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)

    result = clinic.appointments.cancel_appointment('A1')

    assert result is booked
    assert booked.status is AppointmentStatus.CANCELLED
    assert booked.patient is clinic.patient
    assert booked.practitioner is clinic.doctor
    assert booked.date_time == NINE


def test_cancelled_appointment_remains_retrievable(clinic: Clinic) -> None:
    """TS-22: A cancelled appointment isn't deleted; we can still find and
    list it.
    """
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)

    clinic.appointments.cancel_appointment('A1')

    found = clinic.appointments.find_appointment('A1')
    assert found is booked
    assert found.status is AppointmentStatus.CANCELLED
    assert clinic.store.list_appointments() == [booked]


def test_repeated_cancellation_is_rejected_without_change(
    clinic: Clinic,
) -> None:
    """TS-23: Cancelling twice is rejected and the appointment stays
    CANCELLED.
    """
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)
    clinic.appointments.cancel_appointment('A1')

    with pytest.raises(ValueError):
        clinic.appointments.cancel_appointment('A1')

    assert booked.status is AppointmentStatus.CANCELLED
    assert clinic.store.list_appointments() == [booked]


def test_completed_appointment_cancellation_is_rejected(
    clinic: Clinic,
) -> None:
    """TS-24: A COMPLETED appointment can't be cancelled."""
    completed = Appointment(
        'A1', clinic.patient, clinic.doctor, NINE,
        AppointmentStatus.COMPLETED,
    )
    clinic.store.add_appointment(completed)

    with pytest.raises(ValueError):
        clinic.appointments.cancel_appointment('A1')

    assert completed.status is AppointmentStatus.COMPLETED
    assert clinic.appointments.find_appointment('A1') is completed


def test_cancel_unknown_or_blank_id_leaves_appointments_unchanged(
    clinic: Clinic,
) -> None:
    """TS-25: Cancelling an unknown or blank ID fails and leaves other
    appointments alone.
    """
    booked = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)

    with pytest.raises(LookupError):
        clinic.appointments.cancel_appointment('A404')
    with pytest.raises(ValueError):
        clinic.appointments.cancel_appointment('   ')

    assert booked.status is AppointmentStatus.SCHEDULED
    assert clinic.store.list_appointments() == [booked]


def test_cancelling_one_appointment_leaves_others_scheduled(
    clinic: Clinic,
) -> None:
    """TS-26: Cancelling one appointment doesn't affect the others."""
    target = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE)
    other = clinic.appointments.book_appointment('A2', 'P1', 'D2', NINE)

    clinic.appointments.cancel_appointment('A1')

    assert target.status is AppointmentStatus.CANCELLED
    assert other.status is AppointmentStatus.SCHEDULED

def test_stage9_service_listing_and_history(clinic: Clinic):
    # A registered practitioner with no bookings gets an empty list.
    assert clinic.appointments.list_practitioner_appointments("D1") == []

    later = clinic.appointments.book_appointment(
        "A2", "P1", "D1", datetime(2026, 12, 1, 11, 0)
    )
    earlier = clinic.appointments.book_appointment(
        "A1", "P1", "D1", datetime(2026, 12, 1, 9, 0)
    )
    other = clinic.appointments.book_appointment(
        "A3", "P1", "D2", datetime(2026, 12, 1, 9, 0)
    )

    clinic.appointments.cancel_appointment("A1")

    result = clinic.appointments.list_practitioner_appointments("D1")

    assert result == [earlier, later]
    assert result[0] is earlier
    assert earlier.status is AppointmentStatus.CANCELLED

    # Cancellation does not delete the appointment.
    assert clinic.appointments.find_appointment("A1") is earlier

    assert clinic.appointments.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    ) == [later]

    assert clinic.appointments.list_practitioner_appointments(
        "D1", AppointmentStatus.CANCELLED
    ) == [earlier]

    assert clinic.appointments.list_practitioner_appointments(
        "D1", AppointmentStatus.COMPLETED
    ) == []

    assert clinic.appointments.list_practitioner_appointments("D2") == [other]

    # Store insertion order remains unchanged.
    assert clinic.store.list_appointments() == [later, earlier, other]

def test_stage9_service_listing_invalid_inputs(clinic: Clinic):
    appointment = clinic.appointments.book_appointment(
        "A1", "P1", "D1", datetime(2026, 12, 1, 9, 0)
    )

    before = clinic.store.list_appointments()

    # Valid but unregistered practitioner.
    with pytest.raises(LookupError):
        clinic.appointments.list_practitioner_appointments("UNKNOWN")

    # Blank practitioner ID.
    with pytest.raises(ValueError):
        clinic.appointments.list_practitioner_appointments(" ")

    # Invalid practitioner ID type.
    with pytest.raises(ValueError):
        clinic.appointments.list_practitioner_appointments(123)

    # Status must be an AppointmentStatus enum.
    with pytest.raises(ValueError):
        clinic.appointments.list_practitioner_appointments(
            "D1", "scheduled"
        )

    # Failed requests must not change the stored appointment.
    assert clinic.store.list_appointments() == before
    assert clinic.appointments.find_appointment("A1") is appointment
    assert appointment.status is AppointmentStatus.SCHEDULED
