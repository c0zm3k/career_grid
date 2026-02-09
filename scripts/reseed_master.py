import os
import sys
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db, create_app
from app.models import User, Job
from werkzeug.security import generate_password_hash

app = create_app()

def seed_data():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        # 1. Seed Super Admin
        print("Seeding Super Admin...")
        super_admin = User(
            email='superadmin@nilgiricollege.ac.in',
            password=generate_password_hash('SuperAdmin@123', method='pbkdf2:sha256'),
            role='superadmin',
            needs_password_change=False,
            is_approved=True
        )
        db.session.add(super_admin)

        # 2. Seed 5 Regular Admins
        print("Seeding 5 Placement Admins...")
        for i in range(1, 6):
            admin = User(
                email=f'admin{i}@nilgiricollege.ac.in',
                password=generate_password_hash('password123', method='pbkdf2:sha256'),
                role='admin',
                needs_password_change=False,
                is_approved=True
            )
            db.session.add(admin)

        # 3. Seed Jobs & Internships
        print("Seeding 12 diverse Jobs & Internships...")
        jobs_data = [
            # Technology
            ('Full Stack Developer', 'Google', 'Build scalable web applications using Python and React.', 8.5, 30, 'Job'),
            ('Frontend Intern', 'Meta', 'Assist in developing responsive UI components for social platforms.', 7.5, 45, 'Internship'),
            ('Data Analyst', 'Amazon', 'Interpret complex data sets and provide actionable insights.', 8.0, 20, 'Job'),
            ('Cybersecurity Associate', 'Microsoft', 'Monitor networks for security breaches and coordinate response.', 8.2, 25, 'Job'),
            
            # Management & Finance
            ('Financial Consultant', 'Deloitte', 'Provide strategic financial advice to large scale clients.', 7.8, 40, 'Job'),
            ('Marketing Intern', 'HubSpot', 'Help manage social media campaigns and content strategy.', 6.5, 60, 'Internship'),
            ('Project Manager', 'Atlassian', 'Coordinate cross-functional teams to deliver software projects.', 8.5, 15, 'Job'),
            
            # Content & Creative
            ('Content Strategist', 'Netflix', 'Curate and optimize content for global audience engagement.', 7.0, 35, 'Job'),
            ('Graphic Design Intern', 'Adobe', 'Design high-quality visual assets for marketing collateral.', 6.0, 50, 'Internship'),
            
            # Science & Research
            ('Lab Research Assistant', 'Pfizer', 'Support clinical trials and laboratory data collection.', 8.0, 28, 'Job'),
            ('Environmental Consultant', 'GreenTech', 'Analyze environmental impact and suggest sustainable solutions.', 7.5, 33, 'Job'),
            ('AI Ethics Intern', 'OpenAI', 'Research the societal impact of large language models.', 8.8, 42, 'Internship')
        ]

        for title, company, desc, cgpa, days_to_deadline, job_type in jobs_data:
            full_title = f"{title} ({job_type})"
            deadline = datetime.utcnow() + timedelta(days=days_to_deadline)
            job = Job(
                title=full_title,
                company=company,
                description=desc,
                min_cgpa=cgpa,
                deadline=deadline
            )
            db.session.add(job)

        db.session.commit()
        print("\n" + "="*40)
        print("DATABASE RESET AND RE-SEEDED SUCCESSFULLY!")
        print("="*40)
        print("Super Admin: superadmin@nilgiricollege.ac.in / SuperAdmin@123")
        print("Admins: admin1 to admin5 @nilgiricollege.ac.in / password123")
        print("Jobs Seeding: 12 high-quality listings added.")
        print("="*40)

if __name__ == "__main__":
    seed_data()
