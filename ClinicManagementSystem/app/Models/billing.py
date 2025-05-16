# models/billing.py
from models.base import db, TimestampMixin

class Billing(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    items = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled
    paid_at = db.Column(db.DateTime)

    appointment = db.relationship('Appointment', backref='bill')
    patient = db.relationship('Patient')