from . import db
from datetime import datetime
from flask_login import UserMixin

# User Table: Handles Auth for Students and Admins
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='student')  # 'student' or 'admin'
    needs_password_change = db.Column(db.Boolean, default=True) # Force change on first login
    is_approved = db.Column(db.Boolean, default=True) # Default True for students, False for self-signup admins
    
    # Relationship to Profile
    profile = db.relationship('StudentProfile', backref='user', uselist=False)

# Student Portfolio: Academic records & Skills
class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    full_name = db.Column(db.String(150))
    department = db.Column(db.String(100)) # e.g., Arts, Science
    cgpa = db.Column(db.Float)
    skills = db.Column(db.String(500))     # Comma-separated tags
    resume_link = db.Column(db.String(300)) # URL to PDF

# Job Postings: Centralized system with eligibility
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    min_cgpa = db.Column(db.Float, default=0.0) # Eligibility criteria
    deadline = db.Column(db.DateTime, nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)

# Application Tracking: Connecting students to recruiters
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50), default='Applied') # Applied, Shortlisted, Rejected
