from app import create_app, db
from app.models import Job
from datetime import datetime, timedelta
import random

def seed_data():
    app = create_app()
    with app.app_context():
        # Clear existing jobs if any (optional, but the user asked for 30+25)
        # Job.query.delete()
        
        companies = [
            "TechNova Solutions", "Global Finance Corp", "Creative Pulse Media", 
            "Swift Logistics", "EcoBuild Engineering", "Nexus Healthcare", 
            "BlueChip Consulting", "Starlight Hospitality", "Visionary Design Lab", 
            "DataStream Analytics", "Future Power Systems", "Astra Aeronautics"
        ]
        
        domains = [
            "Software Development", "Financial Analysis", "Digital Marketing", 
            "Hardware Engineering", "Data Science", "User Experience Design", 
            "Human Resources", "Supply Chain Management", "Content Writing", 
            "Sales & Operations"
        ]

        # 30 Jobs
        for i in range(1, 31):
            domain = random.choice(domains)
            company = random.choice(companies)
            job = Job(
                title=f"{domain} Specialist - Level {random.randint(1,3)}",
                company=company,
                description=f"Exciting opportunity to join {company} as a {domain} Specialist. Looking for proactive individuals with strong analytical skills. Minimum 2 years experience preferred.",
                min_cgpa=round(random.uniform(6.5, 8.5), 2),
                deadline=datetime.utcnow() + timedelta(days=random.randint(15, 60))
            )
            db.session.add(job)

        # 25 Internships
        for i in range(1, 26):
            domain = random.choice(domains)
            company = random.choice(companies)
            internship = Job(
                title=f"{domain} Intern",
                company=company,
                description=f"Join {company} for a summer internship in {domain}. Gain hands-on experience and work with industry experts. Open to final year students.",
                min_cgpa=round(random.uniform(6.0, 8.0), 2),
                deadline=datetime.utcnow() + timedelta(days=random.randint(10, 45))
            )
            db.session.add(internship)

        db.session.commit()
        print(f"Successfully added 30 jobs and 25 internships.")

if __name__ == "__main__":
    seed_data()
