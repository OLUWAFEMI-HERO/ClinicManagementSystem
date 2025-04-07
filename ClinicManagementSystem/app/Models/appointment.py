from app.__init__ import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    appointment_time = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(200))
    status = db.Column(db.String(50), default="Scheduled")
