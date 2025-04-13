from app.__init__ import db

class Prescription(db.Model):
    __tablename__ = "prescriptions"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    medication = db.Column(db.String(200))
    dosage = db.Column(db.String(100))
    instructions = db.Column(db.String(300))
