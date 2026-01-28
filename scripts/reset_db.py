import os
from app import db, create_app
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
db_path = os.path.join(app.instance_path, 'site.db')

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    
    # Re-seed Admin
    print("Seeding Super Admin...")
    hashed_pw = generate_password_hash('Nilgiri@Admin2026', method='pbkdf2:sha256')
    admin = User(email='admin@nilgiricollege.ac.in', password=hashed_pw, role='superadmin', needs_password_change=False, is_approved=True)
    db.session.add(admin)
    db.session.commit()
    print("Database reset and Admin seeded!")
