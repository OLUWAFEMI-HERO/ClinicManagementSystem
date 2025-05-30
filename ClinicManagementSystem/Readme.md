### Clinic Management System
A complete, full-stack Clinic Management System built with Flask that provides comprehensive healthcare management solutions for modern clinics and small hospitals.

https://img.shields.io/badge/Python-3.10%252B-blue
https://img.shields.io/badge/Flask-2.3%252B-green
https://img.shields.io/badge/License-MIT-yellow
https://img.shields.io/badge/Status-Production%2520Ready-brightgreen

## 🚀 Overview
This Clinic Management System is a robust, scalable solution designed to streamline healthcare operations. It covers every aspect of clinic management from patient registration to discharge summaries, making it perfect for:

Private clinics and polyclinics

Small to medium hospitals

Healthcare startups

Educational institutions (as a learning project)

Built with modern development practices and ready for production deployment with PostgreSQL/MySQL.

## ✨ Key Features
## 🔐 Authentication & Security
JWT-based authentication with 8-hour expiry

Role-based access control (Admin, Doctor, Receptionist)

Password hashing with bcrypt

Secure session management

## 👥 Patient Management
Complete patient registration and profile management

Medical history tracking

Advanced search and filtering

Patient demographics and contact management

## 📅 Appointment System
Intelligent appointment booking

Rescheduling and cancellation

Status tracking (Scheduled, Completed, Cancelled)

Doctor and date-based filtering

## 🏥 Clinical Workflow
Comprehensive clinical records:

Symptoms documentation

Examination findings

Diagnosis and treatment plans

Prescription management with dosage, frequency, and duration

Lab test orders with urgency levels

Discharge summaries with follow-up scheduling

## 🔍 Advanced Features
Powerful search across all modules

Audit trails with automatic timestamps

RESTful API ready for mobile apps

Modular architecture for easy extension

## 🛠 Tech Stack
Layer	Technology
Backend	Python 3.10+, Flask 2.3+
ORM	Flask-SQLAlchemy + Flask-Migrate
Authentication	Flask-JWT-Extended + bcrypt
Database	SQLite (default) → PostgreSQL/MySQL ready
Validation	Pydantic (optional in schemas)
Environment	python-dotenv

## 📁 Project Structure
text
clinic_management_system/
├── main.py                    # Application entry point
├── config/
│   └── database.py            # App factory & database configuration
├── models/                    # SQLAlchemy data models
│   ├── user.py               # User and staff management
│   ├── patient.py            # Patient records
│   ├── appointment.py        # Appointment scheduling
│   ├── clinical_record.py    # Clinical documentation
│   ├── prescription_item.py  # Medication management
│   └── test_order.py         # Lab test orders
├── routes/                    # API endpoints (Blueprints)
│   ├── auth.py               # Authentication routes
│   ├── patients.py           # Patient management
│   ├── appointments.py       # Appointment handling
│   ├── clinical.py           # Clinical workflows
│   └── billing.py            # Future billing module
├── utils/
│   ├── auth.py               # Password hashing & JWT utilities
│   ├── helpers.py            # Common utilities
│   └── seed.py               # Default admin creation
├── static/                    # Frontend assets (CSS, JS, images)
├── templates/                 # Jinja2 templates (optional)
├── .env                       # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # This file

## 🚀 Quick Start
Prerequisites
Python 3.10 or higher

pip (Python package manager)

Installation & Setup (5 Minutes)
Clone the Repository

bash
git clone https://github.com/yourusername/clinic-management-system.git
cd clinic-management-system
Set Up Virtual Environment

bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
Install Dependencies

bash
pip install -r requirements.txt
Run the Application

bash
python main.py
Access the System

Server starts at: http://localhost:5000

You'll see admin credentials in console:

text
Admin user created: admin / admin123
Default Login Credentials
Role	Username	Password	Access Level
Admin	admin	admin123	Full system access
Additional users can be created by admin			

## 📚 API Documentation
Authentication Endpoints
Method	Endpoint	Description	Required Role
POST	/api/auth/login	User login → returns JWT token	Any
POST	/api/auth/register	Register new staff member	Admin
Appointment Management
Method	Endpoint	Description	Parameters
GET	/api/appointments	List appointments	?patient=John&doctor=1&date=2024-01-15
POST	/api/appointments	Book new appointment	JSON payload
PUT	/api/appointments/{id}	Update appointment	JSON payload
DELETE	/api/appointments/{id}	Cancel appointment	-
Patient Management
Method	Endpoint	Description
GET	/api/patients	List all patients
POST	/api/patients	Register new patient
GET	/api/patients/{id}	Get patient details
PUT	/api/patients/{id}	Update patient record
Clinical Records
Method	Endpoint	Description
POST	/api/clinical/{patient_id}	Save diagnosis + prescription + tests
GET	/api/clinical/patient/{patient_id}	Get patient clinical history
Example API Usage:

bash
# Login and get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Use token for subsequent requests
curl -X GET http://localhost:5000/api/appointments \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
🗄 Database Configuration
Using SQLite (Default)
No additional setup required. The system creates the database automatically.

## Switching to PostgreSQL (Production)
Update .env file:

env
## DATABASE_URL=postgresql://username:password@localhost:5432/clinic_db
Run migrations:

bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Database Migrations
The system uses Flask-Migrate for database version control:

bash
# Create new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback if needed
flask db downgrade
🔒 Security Features
Password Security: All passwords hashed with bcrypt

JWT Tokens: Secure authentication with configurable expiry

Role Protection: Route-level authorization checks

SQL Injection Protection: Using SQLAlchemy ORM

Input Validation: Comprehensive data validation
 
## 🎯 Role-Based Access
Role	Permissions
Admin	Full system access, user management, all operations
Doctor	Patient records, clinical documentation, prescriptions
Receptionist	Appointment scheduling, patient registration

## 🚀 Deployment
Development
bash
python main.py
Production with Gunicorn
bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
Docker Deployment (Optional)
dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
## 🔮 Future Enhancements
The system is designed for easy extension. Planned features include:

📄 PDF Generation: Prescription and discharge summaries (ReportLab/WeasyPrint)

📱 Notifications: SMS/Email appointment reminders (Twilio/SendGrid)

🌐 Patient Portal: Self-booking and medical record access

💳 Billing Module: Invoicing and payment tracking

📊 Analytics Dashboard: Reports and insights

📅 Calendar Integration: FullCalendar for visual scheduling

📎 File Uploads: Medical reports and scan storage

## 🤝 Contributing
We welcome contributions! Here's how you can help:

Report Issues: Found a bug? Open an issue with detailed description

Feature Requests: Suggest new features that would benefit clinics

Code Contributions: Submit pull requests for:

Bug fixes

New features

Documentation improvements

Test cases

Development Setup
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit changes: git commit -m 'Add amazing feature'

Push to branch: git push origin feature/amazing-feature

Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.