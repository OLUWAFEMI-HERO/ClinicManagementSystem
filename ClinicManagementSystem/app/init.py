from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    from app.routes.patient_routes import patient_bp
    from app.routes.doctor_routes import doctor_bp
    from app.routes.appointment_routes import appointment_bp
    from app.routes.billing_routes import billing_bp

    app.register_blueprint(patient_bp, url_prefix="/api/patients")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctors")
    app.register_blueprint(appointment_bp, url_prefix="/api/appointments")
    app.register_blueprint(billing_bp, url_prefix="/api/billing")

    return app
