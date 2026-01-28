import os
import sys
import pandas as pd
from werkzeug.security import generate_password_hash

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db, create_app
from app.models import User, StudentProfile

def seed_students(excel_path):
    app = create_app()
    with app.app_context():
        try:
            print(f"Reading {excel_path}...")
            df = pd.read_excel(excel_path)
            
            # Clean columns case-insensitivity
            df.columns = [c.lower().strip() for c in df.columns]
            
            required_cols = ['email', 'full_name', 'department', 'cgpa', 'password']
            if not all(col in df.columns for col in required_cols):
                print(f"Error: Missing columns. Needs {required_cols}")
                return

            print(f"Processing {len(df)} rows...")
            
            added_count = 0
            updated_count = 0
            
            for _, row in df.iterrows():
                email = str(row['email']).strip()
                user = User.query.filter_by(email=email).first()
                
                if not user:
                    # Create User
                    pwd = str(row['password']).strip()
                    hashed = generate_password_hash(pwd, method='pbkdf2:sha256')
                    user = User(
                        email=email,
                        password=hashed,
                        role='student',
                        needs_password_change=True,
                        is_approved=True # Hard-seed students as approved
                    )
                    db.session.add(user)
                    db.session.flush() # Get ID
                    
                    # Create Profile
                    profile = StudentProfile(
                        user_id=user.id,
                        full_name=str(row['full_name']).strip(),
                        department=str(row['department']).strip(),
                        cgpa=float(row['cgpa'])
                    )
                    db.session.add(profile)
                    added_count += 1
                else:
                    # Update Profile if student
                    if user.role == 'student':
                        if not user.profile:
                            user.profile = StudentProfile(user_id=user.id)
                        
                        user.profile.full_name = str(row['full_name']).strip()
                        user.profile.department = str(row['department']).strip()
                        user.profile.cgpa = float(row['cgpa'])
                        updated_count += 1
            
            db.session.commit()
            print(f"Done! Added: {added_count}, Updated: {updated_count}")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), '..', 'test_students.xlsx')
    seed_students(path)
