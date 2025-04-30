# routes/appointments.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.appointment import Appointment, AppointmentStatus
from models.patient import Patient
from models.user import User, Role
from models.base import db
from datetime import datetime
import enum

appointment_bp = Blueprint('appointments', __name__)

# Helper: Role check
def admin_or_doctor_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        role = identity['role']
        if role not in ['admin', 'doctor']:
            return jsonify({"error": "Access denied"}), 403
        return fn(*args, **kwargs)
    return wrapper

# BOOK NEW APPOINTMENT
@appointment_bp.route('', methods=['POST'])
@jwt_required()
def book_appointment():
    data = request.json
    patient = Patient.query.filter_by(phone=data['patient_phone']).first()
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    doctor = User.query.filter_by(id=data['doctor_id'], role=Role.DOCTOR).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        appointment_date=datetime.fromisoformat(data['appointment_date']),
        reason=data.get('reason'),
        notes=data.get('notes')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment booked", "id": appointment.id}), 201

# SEARCH & LIST APPOINTMENTS
@appointment_bp.route('', methods=['GET'])
@jwt_required()
def search_appointments():
    query = Appointment.query

    # Filters
    patient_name = request.args.get('patient')
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    status = request.args.get('status')

    if patient_name:
        query = query.join(Patient).filter(Patient.full_name.ilike(f"%{patient_name}%"))
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        query = query.filter(db.func.date(Appointment.appointment_date) == date_obj.date())
    if status:
        query = query.filter(Appointment.status == status)

    appointments = query.order_by(Appointment.appointment_date.desc()).all()

    result = []
    for appt in appointments:
        result.append({
            "id": appt.id,
            "patient": appt.patient.full_name,
            "doctor": appt.doctor.username,
            "date": appt.appointment_date.isoformat(),
            "status": appt.status.value,
            "reason": appt.reason
        })
    return jsonify(result)

# UPDATE APPOINTMENT (Reschedule / Change Status)
@appointment_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_appointment(id):
    appt = Appointment.query.get_or_404(id)
    data = request.json

    if 'appointment_date' in data:
        appt.appointment_date = datetime.fromisoformat(data['appointment_date'])
    if 'status' in data:
        appt.status = AppointmentStatus(data['status'])
    if 'notes' in data:
        appt.notes = data['notes']

    db.session.commit()
    return jsonify({"message": "Appointment updated"})

# CANCEL / DELETE
@appointment_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(id):
    appt = Appointment.query.get_or_404(id)
    db.session.delete(appt)
    db.session.commit()
    return jsonify({"message": "Appointment deleted"})