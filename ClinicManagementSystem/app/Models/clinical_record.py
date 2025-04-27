# models/clinical_record.py
from models.base import db, TimestampMixin

class ClinicalRecord(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), unique=True)
    diagnosis = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    examination_findings = db.Column(db.Text)
    treatment_plan = db.Column(db.Text)
    follow_up_date = db.Column(db.DateTime)
    is_discharged = db.Column(db.Boolean, default=False)
    discharge_summary = db.Column(db.Text)
    discharge_date = db.Column(db.DateTime)