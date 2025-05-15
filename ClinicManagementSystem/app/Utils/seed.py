from models.user import User, Role, db
from utils.auth import hash_password

def seed_admin():
    if not User.query.filter_by(role=Role.ADMIN).first():
        admin = User(
            username="admin",
            email="admin@clinic.com",
            password_hash=hash_password("admin123"),
            role=Role.ADMIN
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin / admin123")