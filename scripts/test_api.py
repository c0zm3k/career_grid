import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("Testing Career Grid API...")

    # 1. Signup Student (Valid)
    print("\n1. Testing Student Signup (Valid)...")
    res = requests.post(f"{BASE_URL}/signup", json={
        "email": "student@nilgiricollege.ac.in",
        "password": "password123",
        "role": "student"
    })
    print(res.json())

    # 2. Signup Student (Invalid Email)
    print("\n2. Testing Student Signup (Invalid Email)...")
    res = requests.post(f"{BASE_URL}/signup", json={
        "email": "student@gmail.com",
        "password": "password123",
        "role": "student"
    })
    print(res.json())

    # 3. Signup Admin
    print("\n3. Testing Admin Signup...")
    res = requests.post(f"{BASE_URL}/signup", json={
        "email": "admin@careergrid.com",
        "password": "adminpassword",
        "role": "admin"
    })
    print(res.json())

    # 4. Login Student
    print("\n4. Testing Student Login...")
    session = requests.Session()
    res = session.post(f"{BASE_URL}/login", json={
        "email": "student@nilgiricollege.ac.in",
        "password": "password123"
    })
    print(res.json())

    # 5. Update Portfolio
    print("\n5. Testing Portfolio Update...")
    res = session.post(f"{BASE_URL}/portfolio", json={
        "full_name": "Test Student",
        "cgpa": 8.5,
        "skills": "Python, Flask, SQL",
        "department": "Computer Science",
        "resume_link": "https://example.com/resume.pdf"
    })
    print(res.json())

    # 6. Admin Posting Job
    print("\n6. Testing Admin Job Posting...")
    admin_session = requests.Session()
    admin_session.post(f"{BASE_URL}/login", json={
        "email": "admin@careergrid.com",
        "password": "adminpassword"
    })
    deadline = "2026-12-31T23:59:59"
    res = admin_session.post(f"{BASE_URL}/jobs", json={
        "title": "Software Engineer Intern",
        "company": "Tech Corp",
        "description": "Awesome internship",
        "min_cgpa": 8.0,
        "deadline": deadline
    })
    job_data = res.json()
    print(job_data)
    job_id = job_data.get('job_id')

    # 7. Student Applying for Job (Meet criteria)
    print("\n7. Testing Student Job Application (Eligible)...")
    res = session.post(f"{BASE_URL}/apply/{job_id}")
    print(res.json())

    # 8. Chatbot Test
    print("\n8. Testing Chatbot...")
    res = requests.post(f"{BASE_URL}/chatbot", json={"message": "What is the contact email?"})
    print(res.json())

    print("\nTests completed.")

if __name__ == "__main__":
    test_api()
