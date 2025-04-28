class PrescriptionItem(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    clinical_record_id = db.Column(db.Integer, db.ForeignKey('clinical_record.id'))
    drug_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    instructions = db.Column(db.Text)

    clinical_record = db.relationship('ClinicalRecord', backref='prescriptions')