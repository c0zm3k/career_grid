"""
Quick diagnostic to test the student update flow
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

# Login as admin
session = requests.Session()
login_res = session.post(f"{BASE_URL}/login", json={
    "email": "admin@nilgiricollege.ac.in",
    "password": "admin123"
})

print(f"Login Status: {login_res.status_code}")

# Try updating student profile ID 1
update_res = session.post(f"{BASE_URL}/api/admin/student/update/1", json={
    "department": "Computer Science",
    "cgpa": 8.87
})

print(f"Update Status: {update_res.status_code}")
print(f"Update Response: {update_res.json()}")

# Verify in database
from app import create_app
from app.models import StudentProfile

app = create_app()
with app.app_context():
    profile = StudentProfile.query.get(1)
    print(f"\nDatabase State:")
    print(f"  Name: {profile.full_name}")
    print(f"  Dept: {profile.department}")
    print(f"  CGPA: {profile.cgpa}")
