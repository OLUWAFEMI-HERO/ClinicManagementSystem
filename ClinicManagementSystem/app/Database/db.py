from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.patients import patient_bp
    from routes.doctors import doctor_bp
    from routes.appointments import appointment_bp
    from routes.prescriptions import prescription_bp
    from routes.billing import billing_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patients')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctors')
    app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
    app.register_blueprint(prescription_bp, url_prefix='/api/prescriptions')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')

    return app