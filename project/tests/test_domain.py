"""Tests for Patient, Practitioner and Appointment on their own.
"""

from datetime import datetime, timedelta, timezone

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


WHEN = datetime(2026, 10, 1, 9, 0)


def make_appointment(
    status: AppointmentStatus = AppointmentStatus.SCHEDULED,
) -> Appointment:
    """Make a fresh appointment for P1 with D1 at 9am."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    return Appointment('A1', patient, practitioner, WHEN, status)


# --- Patient ---

def test_valid_patient_stores_trimmed_fields() -> None:
    """TD-01: A valid patient keeps its ID and name, with extra spaces removed."""
    patient = Patient('  P1  ', '  Alex Example  ')

    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


@pytest.mark.parametrize('bad_id', ['', '   ', '\t\n', None, 101])
def test_blank_patient_id_is_rejected(bad_id: object) -> None:
    """TD-02: A blank or non-text patient ID is rejected."""
    with pytest.raises(ValueError):
        Patient(bad_id, 'Alex Example')


@pytest.mark.parametrize('bad_name', ['', '   ', None])
def test_blank_patient_name_is_rejected(bad_name: object) -> None:
    """TD-03: A patient must have a name."""
    with pytest.raises(ValueError):
        Patient('P1', bad_name)


# --- Practitioner ---

def test_valid_practitioner_stores_trimmed_fields() -> None:
    """TD-04: A valid practitioner keeps its ID, name and specialty, trimmed."""
    practitioner = Practitioner(' D1 ', ' Taylor Example ', ' General ')

    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General'


@pytest.mark.parametrize(
    ('practitioner_id', 'name', 'specialty'),
    [
        ('', 'Taylor Example', 'General'),
        ('   ', 'Taylor Example', 'General'),
        ('D1', '', 'General'),
        ('D1', '   ', 'General'),
        ('D1', 'Taylor Example', ''),
        ('D1', 'Taylor Example', '   '),
    ],
)
def test_blank_practitioner_fields_are_rejected(
    practitioner_id: str,
    name: str,
    specialty: str,
) -> None:
    """TD-05: A practitioner needs an ID, a name and a specialty."""
    with pytest.raises(ValueError):
        Practitioner(practitioner_id, name, specialty)


# --- Appointment construction ---

def test_new_appointment_starts_scheduled() -> None:
    """TD-06: A new appointment starts as SCHEDULED and keeps the patient,
    practitioner and time it was given.
    """
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')

    appointment = Appointment(' A1 ', patient, practitioner, WHEN)

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == WHEN


@pytest.mark.parametrize('bad_id', ['', '   ', None])
def test_blank_appointment_id_is_rejected(bad_id: object) -> None:
    """TD-07: An appointment must have an ID."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')

    with pytest.raises(ValueError):
        Appointment(bad_id, patient, practitioner, WHEN)


def test_appointment_requires_real_participant_objects() -> None:
    """TD-08: An appointment needs real Patient and Practitioner objects, not
    just their IDs.
    """
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')

    with pytest.raises(ValueError):
        Appointment('A1', 'P1', practitioner, WHEN)
    with pytest.raises(ValueError):
        Appointment('A1', patient, 'D1', WHEN)
    with pytest.raises(ValueError):
        Appointment('A1', practitioner, patient, WHEN)


@pytest.mark.parametrize(
    'bad_time',
    [
        datetime(2026, 10, 1, 9, 0, tzinfo=timezone(timedelta(hours=11))),
        datetime(2026, 10, 1, 9, 0, 1),
        datetime(2026, 10, 1, 9, 0, 0, 1),
        '2026-10-01 09:00',
        None,
    ],
    ids=['timezone-aware', 'nonzero-second', 'nonzero-microsecond',
         'text', 'none'],
)
def test_invalid_appointment_time_is_rejected(bad_time: object) -> None:
    """TD-09: Times with a timezone, seconds or the wrong type are rejected."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')

    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, bad_time)


def test_minute_precision_time_is_accepted() -> None:
    """TD-10: A normal time to the minute, like 11:59pm, is accepted."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    edge = datetime(2026, 10, 1, 23, 59)

    appointment = Appointment('A1', patient, practitioner, edge)

    assert appointment.date_time == edge


def test_non_enum_status_is_rejected() -> None:
    """TD-11: The status must be an AppointmentStatus, not plain text."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')

    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, WHEN, 'scheduled')


def test_identity_and_status_are_read_only() -> None:
    """TD-12: IDs and status can't be changed directly; only cancel() changes
    the status.
    """
    appointment = make_appointment()

    with pytest.raises(AttributeError):
        appointment.patient.patient_id = 'P2'
    with pytest.raises(AttributeError):
        appointment.practitioner.practitioner_id = 'D2'
    with pytest.raises(AttributeError):
        appointment.appointment_id = 'A2'
    with pytest.raises(AttributeError):
        appointment.status = AppointmentStatus.CANCELLED

    assert appointment.patient.patient_id == 'P1'
    assert appointment.appointment_id == 'A1'
    assert appointment.status is AppointmentStatus.SCHEDULED


# --- Appointment cancellation -------------------------------------------

def test_cancel_changes_status() -> None:
    """TD-13: Cancelling changes the status to CANCELLED and nothing else."""
    appointment = make_appointment()
    patient = appointment.patient
    practitioner = appointment.practitioner

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == WHEN


def test_repeated_cancellation_is_rejected() -> None:
    """TD-14: Cancelling twice is rejected and the appointment stays CANCELLED."""
    appointment = make_appointment()
    appointment.cancel()

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


def test_completed_appointment_cannot_be_cancelled() -> None:
    """TD-15: A COMPLETED appointment can't be cancelled."""
    appointment = make_appointment(AppointmentStatus.COMPLETED)

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.COMPLETED