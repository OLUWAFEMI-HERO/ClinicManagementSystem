class TestOrder(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    clinical_record_id = db.Column(db.Integer, db.ForeignKey('clinical_record.id'))
    test_name = db.Column(db.String(100), nullable=False)
    urgency = db.Column(db.String(20), default="routine")  # routine, urgent, stat
    notes = db.Column(db.Text)
    result = db.Column(db.Text)
    result_date = db.Column(db.DateTime)

    clinical_record = db.relationship('ClinicalRecord', backref='tests')