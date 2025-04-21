from app.models.patient import Patient
from app.__init__ import db

def create_patient(data):
    patient = Patient(**data)
    db.session.add(patient)
    db.session.commit()
    return patient

def get_all_patients():
    return Patient.query.all()

def get_patient_by_id(patient_id):
    return Patient.query.get(patient_id)
