from app.models.doctor import Doctor
from app.__init__ import db

def create_doctor(data):
    doctor = Doctor(**data)
    db.session.add(doctor)
    db.session.commit()
    return doctor

def get_all_doctors():
    return Doctor.query.all()
