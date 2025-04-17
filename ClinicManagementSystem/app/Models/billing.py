from app.__init__ import db
from datetime import datetime

class Billing(db.Model):
    __tablename__ = "billing"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    amount = db.Column(db.Float)
    status = db.Column(db.String(50), default="Unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
