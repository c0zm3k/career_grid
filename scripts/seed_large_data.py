import os
import sys
from datetime import datetime, timedelta
import random

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db, create_app
from app.models import Job

def seed_large_data():
    app = create_app()
    with app.app_context():
        print("Seeding diverse jobs and internships...")
        
        # Domains and Companies
        domains = [
            ("Tech", ["Google", "Microsoft", "Amazon", "Meta", "TCS", "Infosys", "Wipro", "Zoho"]),
            ("Finance", ["HDFCBank", "ICICI Bank", "Goldman Sachs", "J.P. Morgan", "Deloitte", "KPMG"]),
            ("Healthcare", ["Apollo Hospitals", "Pfizer", "Cipla", "Reddy's Labs", "Sun Pharma"]),
            ("Education", ["Byju's", "Unacademy", "Khan Academy", "Pearson", "Coursera"]),
            ("Retail", ["Reliance", "Tata Cliq", "Amazon Retail", "Flipkart", "Walmart"]),
            ("Creative", ["Adobe", "Canva", "Pixar", "Digital Art Studio", "Marketing Pro"])
        ]

        job_titles = [
            "Software Engineer", "Backend Developer", "Frontend Developer", "Data Scientist", 
            "Project Manager", "Business Analyst", "System Architect", "DevOps Engineer",
            "QA Engineer", "Mobile App Developer", "Cybersecurity Analyst", "Cloud Architect",
            "UX/UI Designer", "Content Writer", "HR Manager", "Operations Specialist",
            "Sales Executive", "Marketing Coordinator", "Financial Analyst", "Accountant",
            "Data Entry Specialist", "Customer Support Lead", "Researcher", "Lab Assistant",
            "Teacher", "Academics Coordinator", "Inventory Manager", "Logistics Lead",
            "Digital Marketer", "Social Media Manager"
        ]

        internship_titles = [
            "Software Development Intern", "Data Analytics Intern", "Marketing Intern", 
            "Finance Operations Intern", "HR Recruitment Intern", "Graphic Design Intern",
            "Content Writing Intern", "Business Development Intern", "Research Intern",
            "Product Management Intern", "UI/UX Design Intern", "Quality Assurance Intern"
        ]

        added_count = 0

        # Seed 30+ Jobs
        for i in range(35):
            domain, companies = random.choice(domains)
            title = random.choice(job_titles)
            company = random.choice(companies)
            min_cgpa = round(random.uniform(6.0, 8.5), 1)
            deadline = datetime.utcnow() + timedelta(days=random.randint(15, 60))
            
            job = Job(
                title=f"{title} ({domain})",
                company=company,
                description=f"Join {company} as a {title}. We are looking for talented individuals in the {domain} sector. Key responsibilities include managing projects, collaborating with teams, and delivering high-quality results. Requires strong communication skills and a passion for excellence in {domain}.",
                min_cgpa=min_cgpa,
                deadline=deadline
            )
            db.session.add(job)
            added_count += 1

        # Seed 25+ Internships
        for i in range(28):
            domain, companies = random.choice(domains)
            title = random.choice(internship_titles)
            company = random.choice(companies)
            min_cgpa = round(random.uniform(5.5, 7.5), 1)
            deadline = datetime.utcnow() + timedelta(days=random.randint(10, 45))
            
            internship = Job(
                title=f"{title} - {domain}",
                company=company,
                description=f"Exciting internship opportunity at {company}! As a {title} in the {domain} department, you will gain hands-on experience, work on real-world projects, and be mentored by industry experts. This is a 3-6 month program designed for students to explore {domain} careers.",
                min_cgpa=min_cgpa,
                deadline=deadline
            )
            db.session.add(internship)
            added_count += 1

        db.session.commit()
        print(f"Successfully seeded {added_count} opportunities!")

if __name__ == "__main__":
    seed_large_data()
