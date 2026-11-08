
from datetime import datetime

from smartcare.domain import (
    Patient, Practitioner, Appointment, AppointmentStatus
)
from smartcare.queries import appointment_sort_key, select_appointments


def test_appointments_sorted_by_date_time():
    patient = Patient("P1", "Alex")
    doctor = Practitioner("D1", "Taylor", "General")

    later = Appointment(
        "A2", patient, doctor, datetime(2026, 12, 1, 11, 0)
    )
    earlier = Appointment(
        "A1", patient, doctor, datetime(2026, 12, 1, 9, 0)
    )

    original = [later, earlier]

    result = select_appointments(original, "D1")

    assert result == [earlier, later]
    assert original == [later, earlier]
    assert result is not original
    assert result[0] is earlier
    assert appointment_sort_key(earlier) < appointment_sort_key(later)

def test_practitioner_filter_and_id_tie_break():
    patient = Patient("P1", "Alex")
    doctor1 = Practitioner("D1", "Taylor", "General")
    doctor2 = Practitioner("D2", "Smith", "Dental")

    same_time = datetime(2026, 12, 1, 10, 0)

    appointment2 = Appointment(
    "A2", patient, doctor1, same_time,
    status=AppointmentStatus.COMPLETED
)

    other_doctor = Appointment("A0", patient, doctor2, same_time)

    appointment1 = Appointment(
        "A1", patient, doctor1, same_time,
        status=AppointmentStatus.CANCELLED
)

    original = [appointment2, other_doctor, appointment1]

    result = select_appointments(original, "D1")

    assert result == [appointment1, appointment2]
    assert other_doctor not in result
    assert original == [appointment2, other_doctor, appointment1]
    assert result[0] is appointment1

def test_query_returns_fresh_lists():
    patient = Patient("P1", "Alex")
    doctor = Practitioner("D1", "Taylor", "General")

    appointment = Appointment(
        "A1", patient, doctor, datetime(2026, 12, 1, 9, 0)
    )

    original = [appointment]

    result1 = select_appointments(original, "D1")
    result2 = select_appointments(original, "D1")

    assert result1 == result2
    assert result1 is not result2
    assert result1 is not original
    assert result1[0] is appointment

    empty1 = select_appointments(original, "D2")
    empty2 = select_appointments(original, "D2")

    assert empty1 == []
    assert empty2 == []
    assert empty1 is not empty2

    assert select_appointments([], "D1") == []

def test_appointment_status_filtering():
    patient = Patient("P1", "Alex")
    doctor = Practitioner("D1", "Taylor", "General")

    scheduled = Appointment(
        "A1", patient, doctor, datetime(2026, 12, 1, 9, 0)
    )

    cancelled = Appointment(
        "A2", patient, doctor, datetime(2026, 12, 1, 10, 0)
    )
    cancelled.cancel()

    completed = Appointment(
        "A3", patient, doctor, datetime(2026, 12, 1, 11, 0),
        status=AppointmentStatus.COMPLETED
    )

    appointments = [completed, cancelled, scheduled]

    # Default filter includes all statuses.
    assert select_appointments(appointments, "D1") == [
        scheduled, cancelled, completed
    ]

    # Explicit filters return only matching statuses.
    assert select_appointments(
        appointments, "D1", AppointmentStatus.SCHEDULED
    ) == [scheduled]

    assert select_appointments(
        appointments, "D1", AppointmentStatus.CANCELLED
    ) == [cancelled]

    assert select_appointments(
        appointments, "D1", AppointmentStatus.COMPLETED
    ) == [completed]

    # Original list and statuses remain unchanged.
    assert appointments == [completed, cancelled, scheduled]
    assert scheduled.status is AppointmentStatus.SCHEDULED
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert completed.status is AppointmentStatus.COMPLETED
