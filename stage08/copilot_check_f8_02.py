"""F8-01 evidence checks. Run with: python stage08/copilot_check_f8_02.py"""
import sys
from pathlib import Path

# Let this script find the smartcare package in project/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'project'))
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.services import AppointmentService, PatientService, PractitionerService
import smartcare.data_store as ds

store = SmartCareDataStore()
PatientService(store).register_patient('P1', 'Alex Example')
PractitionerService(store).register_practitioner('D1', 'Taylor Example', 'General')
appointments = AppointmentService(store)
booked = appointments.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0))
appointments.cancel_appointment('A1')

listed = store.list_appointments()
print('Check 1 - stored object after cancel:')
print('  in list_appointments():', booked in listed)
print('  listed object is the original booked object:', listed[0] is booked)
print('  ID / status:', listed[0].appointment_id, listed[0].status)
print('Check 2 - lookup in the same store:')
print("  store.find_appointment('A1') ->", store.find_appointment('A1'))
try:
    appointments.find_appointment('A1')
    print("  service.find_appointment('A1') -> found")
except LookupError as error:
    print("  service.find_appointment('A1') -> LookupError:", error)
print('Check 3 - module loaded from:', ds.__file__)