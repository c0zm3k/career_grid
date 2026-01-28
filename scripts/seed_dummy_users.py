from app import create_app, db
from app.models import User, StudentProfile
from werkzeug.security import generate_password_hash
import random

app = create_app()

def seed_mass_users():
    with app.app_context():
        print("Starting mass user seeding...")
        
        # Lists for random generation
        depts = ["Computer Science", "Arts", "Science", "Business", "Engineering"]
        skills_list = ["Python", "JavaScript", "SQL", "Communication", "Java", "C++", "Graphic Design", "Marketing", "Data Analysis", "React"]
        
        credentials = []

        # 1. Clear existing users (optional, but good for clean seed)
        # User.query.delete() 
        # StudentProfile.query.delete()

        # 2. Seed Super Admin
        sa_email = "superadmin@nilgiricollege.ac.in"
        if not User.query.filter_by(email=sa_email).first():
            sa = User(email=sa_email, password=generate_password_hash("superadmin123", method='pbkdf2:sha256'), role="superadmin")
            db.session.add(sa)
            credentials.append(f"Super Admin | {sa_email} | superadmin123")

        # 3. Seed Admins (5)
        for i in range(1, 6):
            adm_email = f"admin{i}@nilgiricollege.ac.in"
            if not User.query.filter_by(email=adm_email).first():
                adm = User(email=adm_email, password=generate_password_hash("password123", method='pbkdf2:sha256'), role="admin")
                db.session.add(adm)
                credentials.append(f"Admin {i} | {adm_email} | password123")

        # 4. Seed Students (50)
        for i in range(1, 51):
            stu_email = f"student{i}@nilgiricollege.ac.in"
            if not User.query.filter_by(email=stu_email).first():
                stu = User(email=stu_email, password=generate_password_hash("password123", method='pbkdf2:sha256'), role="student")
                db.session.add(stu)
                db.session.flush() # Get student id

                # Create profile
                profile = StudentProfile(
                    user_id=stu.id,
                    full_name=f"Student Name {i}",
                    department=random.choice(depts),
                    cgpa=round(random.uniform(6.0, 9.8), 2),
                    skills=", ".join(random.sample(skills_list, 3)),
                    resume_link=f"https://example.com/resume_student_{i}.pdf"
                )
                db.session.add(profile)
                credentials.append(f"Student {i} | {stu_email} | password123")

        db.session.commit()
        
        # 5. Write credentials to file
        with open("login_credentials.txt", "w") as f:
            f.write("CAREER GRID - LOGIN CREDENTIALS REGISTRY\n")
            f.write("="*40 + "\n\n")
            f.write("\n".join(credentials))
        
        print(f"Successfully seeded {len(credentials)} users.")
        print("Credentials saved to login_credentials.txt")

if __name__ == "__main__":
    seed_mass_users()
