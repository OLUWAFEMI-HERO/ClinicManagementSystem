from app.__init__ import db
from datetime import date

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, default=date.today)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(200))

    appointments = db.relationship("Appointment", backref="patient", lazy=True)
