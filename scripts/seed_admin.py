from app import db, create_app
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Only create if not exists
    if not User.query.filter_by(email='superadmin@nilgiricollege.ac.in').first():
        hashed_pw = generate_password_hash('superadmin123', method='pbkdf2:sha256')
        admin = User(email='superadmin@nilgiricollege.ac.in', password=hashed_pw, role='superadmin', needs_password_change=False)
        db.session.add(admin)
        db.session.commit()
        print("Super Admin seeded successfully!")
    else:
        print("Super Admin already exists.")
