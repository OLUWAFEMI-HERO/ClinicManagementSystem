from app.models.appointment import Appointment
from app.__init__ import db

def create_appointment(data):
    appointment = Appointment(**data)
    db.session.add(appointment)
    db.session.commit()
    return appointment

def get_all_appointments():
    return Appointment.query.all()
