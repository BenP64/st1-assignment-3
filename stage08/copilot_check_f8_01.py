"""F8-01 evidence checks. Run with: python stage08/copilot_check_f8_01.py"""
import sys
from pathlib import Path

# Let this script find the smartcare package in project/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'project'))
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.services import AppointmentService, PatientService, PractitionerService

WHEN = datetime(2026, 10, 1, 9, 0)
store = SmartCareDataStore()
PatientService(store).register_patient('P1', 'Alex Example')
PractitionerService(store).register_practitioner('D1', 'Taylor Example', 'General')
PractitionerService(store).register_practitioner('D2', 'Morgan Example', 'General')
AppointmentService(store).book_appointment('A1', 'P1', 'D1', WHEN)

print('Check 1 - store method called directly (no service):')
print('  has_practitioner_conflict(D1, 09:00) =', store.has_practitioner_conflict('D1', WHEN), '(expected True)')
print('  has_practitioner_conflict(D2, 09:00) =', store.has_practitioner_conflict('D2', WHEN), '(expected False)')

print('Check 2 - stored data after booking A1:')
for a in store.list_appointments():
    print('  ', a.appointment_id, a.practitioner.practitioner_id, a.date_time, a.status)

import smartcare.data_store as ds
print('Check 3 - module loaded from:', ds.__file__)