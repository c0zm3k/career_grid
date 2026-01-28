from app import create_app, db
from app.models import User, Job
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()

def seed():
    with app.app_context():
        # 1. Create Admin User
        admin_email = "admin@nilgiricollege.ac.in"
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                password=generate_password_hash("admin_nc_2026", method='pbkdf2:sha256'),
                role="admin"
            )
            db.session.add(admin)
            print(f"Admin user created: {admin_email}")
        else:
            print(f"Admin user {admin_email} already exists.")

        # 2. Add Demo Jobs
        demo_jobs = [
            {
                "title": "Software Engineer Intern",
                "company": "Google",
                "description": "Join the Google engineering team for a summer internship. Work on large scale systems and impact millions of users.",
                "min_cgpa": 8.0,
                "deadline": datetime.now() + timedelta(days=30)
            },
            {
                "title": "Data Analyst",
                "company": "TCS",
                "description": "Looking for freshers with strong analytical skills. Proficiency in Excel, SQL and Python is a plus.",
                "min_cgpa": 7.0,
                "deadline": datetime.now() + timedelta(days=15)
            },
            {
                "title": "Digital Marketing Specialist",
                "company": "Amazon",
                "description": "Manage social media campaigns and analyze traffic patterns. Creativity and data-driven mindset required.",
                "min_cgpa": 6.5,
                "deadline": datetime.now() + timedelta(days=20)
            },
            {
                "title": "Python Developer",
                "company": "Tech Solutions",
                "description": "Backend development using Flask/Django. Experience with REST APIs and databases required.",
                "min_cgpa": 7.5,
                "deadline": datetime.now() + timedelta(days=45)
            },
            {
                "title": "UI/UX Designer",
                "company": "Microsoft",
                "description": "Design user interfaces for diverse product lines. Proficiency in Figma and Adobe XD.",
                "min_cgpa": 8.2,
                "deadline": datetime.now() + timedelta(days=10)
            }
        ]

        for job_data in demo_jobs:
            if not Job.query.filter_by(title=job_data["title"], company=job_data["company"]).first():
                job = Job(**job_data)
                db.session.add(job)
                print(f"Job added: {job_data['title']} at {job_data['company']}")
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
