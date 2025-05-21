# routes/patients.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.patient import Patient
from models.base import db
from datetime import datetime

patient_bp = Blueprint('patients', __name__)

# CREATE NEW PATIENT
@patient_bp.route('', methods=['POST'])
@jwt_required()
def create_patient():
    data = request.get_json()
    if Patient.query.filter_by(phone=data.get('phone')).first():
        return jsonify({"error": "Patient with this phone already exists"}), 400

    patient = Patient(
        full_name=data['full_name'],
        phone=data['phone'],
        email=data.get('email'),
        date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d') if data.get('date_of_birth') else None,
        gender=data.get('gender'),
        address=data.get('address'),
        medical_history=data.get('medical_history')
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({"message": "Patient created", "id": patient.id}), 201


# GET ALL PATIENTS or SEARCH
@patient_bp.route('', methods=['GET'])
@jwt_required()
def list_patients():
    query = Patient.query
    search = request.args.get('search')
    if search:
        query = query.filter(
            db.or_(
                Patient.full_name.ilike(f"%{search}%"),
                Patient.phone.ilike(f"%{search}%"),
                Patient.email.ilike(f"%{search}%")
            )
        )
    patients = query.order_by(Patient.full_name).all()
    result = [{
        "id": p.id,
        "full_name": p.full_name,
        "phone": p.phone,
        "email": p.email,
        "gender": p.gender,
        "date_of_birth": p.date_of_birth.isoformat() if p.date_of_birth else None,
        "address": p.address
    } for p in patients]
    return jsonify(result)


# GET SINGLE PATIENT + VISIT HISTORY
@patient_bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    appointments = [{
        "id": a.id,
        "date": a.appointment_date.isoformat(),
        "doctor": a.doctor.username,
        "status": a.status.value,
        "diagnosis": a.clinical_record.diagnosis if a.clinical_record else None
    } for a in patient.appointments]

    return jsonify({
        "id": patient.id,
        "full_name": patient.full_name,
        "phone": patient.phone,
        "email": patient.email,
        "gender": patient.gender,
        "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        "address": patient.address,
        "medical_history": patient.medical_history,
        "appointments": appointments
    })


# UPDATE PATIENT
@patient_bp.route('/<int:patient_id>', methods=['PUT'])
@jwt_required()
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()

    patient.full_name = data.get('full_name', patient.full_name)
    patient.phone = data.get('phone', patient.phone)
    patient.email = data.get('email', patient.email)
    patient.address = data.get('address', patient.address)
    patient.medical_history = data.get('medical_history', patient.medical_history)

    db.session.commit()
    return jsonify({"message": "Patient updated"})


# DELETE PATIENT (soft or hard – here hard delete)
@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted"})