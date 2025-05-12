from models.base import db, TimestampMixin
import enum

class Role(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    RECEPTIONIST = "receptionist"

class User(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.RECEPTIONIST)
    is_active = db.Column(db.Boolean, default=True)