import requests
import os
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"

def test_student_password_upload():
    session = requests.Session()
    
    # 1. Login as Admin
    print("Logging in as Admin...")
    session.post(f"{BASE_URL}/login", json={
        "email": "admin@nilgiricollege.ac.in",
        "password": "admin123"
    })
    
    # 2. Upload test_students.xlsx
    print("Uploading test_students.xlsx...")
    file_path = "test_students.xlsx"
    with open(file_path, 'rb') as f:
        res = session.post(f"{BASE_URL}/admin/upload-students", files={'file': f})
    print(f"Upload Result: {res.json()}")
    assert res.status_code == 200
    
    # 3. Verify Login with custom password
    print("Verifying student login with custom password...")
    res = requests.post(f"{BASE_URL}/login", json={
        "email": "teststudent1@nilgiricollege.ac.in",
        "password": "student123"
    })
    print(f"Login Result for student 1: {res.json()}")
    assert res.status_code == 200
    assert res.json().get('needs_password_change') is True
    
    res = requests.post(f"{BASE_URL}/login", json={
        "email": "teststudent2@nilgiricollege.ac.in",
        "password": "student456"
    })
    print(f"Login Result for student 2: {res.json()}")
    assert res.status_code == 200
    
    print("\nStudent Password Upload Verification Successful!")

if __name__ == "__main__":
    # First ensure we have an admin and a clean state
    # We'll use the superadmin to create an admin first
    sa_session = requests.Session()
    sa_session.post(f"{BASE_URL}/login", json={"email": "superadmin@nilgiricollege.ac.in", "password": "superadmin123"})
    sa_session.post(f"{BASE_URL}/api/admin/create", json={"email": "admin@nilgiricollege.ac.in", "password": "admin123"})
    sa_session.post(f"{BASE_URL}/api/admin/approve/2") # Assuming ID 2 is the new admin

    try:
        test_student_password_upload()
    except Exception as e:
        print(f"\nVerification Failed: {e}")
