# routes/billing.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.billing import Billing
from models.appointment import Appointment
from models.base import db
from datetime import datetime

billing_bp = Blueprint('billing', __name__)

# CREATE INVOICE AFTER VISIT
@billing_bp.route('/appointment/<int:appointment_id>', methods=['POST'])
@jwt_required()
def create_bill_from_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.status != 'completed':
        return jsonify({"error": "Appointment must be completed first"}), 400

    data = request.get_json()
    bill = Billing(
        appointment_id=appointment_id,
        patient_id=appointment.patient_id,
        items=data.get('items', 'Consultation'),
        amount=data['amount'],
        tax=data.get('tax', 0),
        discount=data.get('discount', 0),
        total_amount=data['amount'] + data.get('tax', 0) - data.get('discount', 0),
        status='pending',
        due_date=datetime.utcnow()
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify({"message": "Invoice created", "bill_id": bill.id}), 201


# MARK AS PAID
@billing_bp.route('/<int:bill_id>/pay', methods=['POST'])
@jwt_required()
def mark_paid(bill_id):
    bill = Billing.query.get_or_404(bill_id)
    bill.status = 'paid'
    bill.paid_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Payment recorded"})


# GET ALL BILLS (filter by patient or status)
@billing_bp.route('', methods=['GET'])
@jwt_required()
def list_bills():
    query = Billing.query
    patient_id = request.args.get('patient_id')
    status = request.args.get('status')

    if patient_id:
        query = query.filter_by(patient_id=patient_id)
    if status:
        query = query.filter_by(status=status)

    bills = query.all()
    result = [{
        "id": b.id,
        "patient": b.patient.full_name,
        "amount": b.amount,
        "total": b.total_amount,
        "status": b.status,
        "date": b.created_at.isoformat()
    } for b in bills]
    return jsonify(result)