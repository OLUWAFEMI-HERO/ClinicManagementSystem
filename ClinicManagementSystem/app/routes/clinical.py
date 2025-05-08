# routes/clinical.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.clinical_record import ClinicalRecord
from models.prescription_item import PrescriptionItem
from models.test_order import TestOrder
from models.appointment import Appointment
from models.base import db

clinical_bp = Blueprint('clinical', __name__)

@clinical_bp.route('/<int:appointment_id>', methods=['POST'])
@jwt_required()
def create_clinical_record(appointment_id):
    identity = get_jwt_identity()
    if identity['role'] != 'doctor':
        return jsonify({"error": "Only doctors can create records"}), 403

    appt = Appointment.query.get_or_404(appointment_id)
    if appt.clinical_record:
        return jsonify({"error": "Record already exists"}), 400

    data = request.json
    record = ClinicalRecord(
        appointment_id=appointment_id,
        diagnosis=data['diagnosis'],
        symptoms=data.get('symptoms'),
        examination_findings=data.get('examination_findings'),
        treatment_plan=data.get('treatment_plan'),
        follow_up_date=data.get('follow_up_date')
    )
    db.session.add(record)
    db.session.flush()

    # Add prescriptions
    for drug in data.get('prescriptions', []):
        item = PrescriptionItem(
            clinical_record_id=record.id,
            drug_name=drug['drug_name'],
            dosage=drug['dosage'],
            frequency=drug['frequency'],
            duration=drug['duration'],
            instructions=drug.get('instructions')
        )
        db.session.add(item)

    # Add tests
    for test in data.get('tests', []):
        t = TestOrder(
            clinical_record_id=record.id,
            test_name=test['test_name'],
            urgency=test.get('urgency', 'routine'),
            notes=test.get('notes')
        )
        db.session.add(t)

    # Discharge?
    if data.get('discharge'):
        record.is_discharged = True
        record.discharge_summary = data['discharge_summary']
        record.discharge_date = datetime.utcnow()
        appt.status = 'completed'

    db.session.commit()
    return jsonify({"message": "Clinical record saved", "record_id": record.id})