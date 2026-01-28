import requests

BASE_URL = "http://127.0.0.1:5000"

def test_flow():
    session = requests.Session()
    
    # 1. Admin Login
    print("Testing Admin Login...")
    res = session.post(f"{BASE_URL}/login", json={
        "email": "superadmin@nilgiricollege.ac.in",
        "password": "superadmin123"
    })
    print(res.json())
    assert res.status_code == 200
    assert res.json()['role'] == 'superadmin'
    
    # 2. Upload Excel
    print("\nTesting Excel Upload...")
    with open('test_students.xlsx', 'rb') as f:
        res = session.post(f"{BASE_URL}/admin/upload-students", files={'file': f})
    print(res.json())
    assert res.status_code == 200
    
    # 3. Student First Login
    print("\nTesting Student First Login...")
    student_session = requests.Session()
    res = student_session.post(f"{BASE_URL}/login", json={
        "email": "teststudent1@nilgiricollege.ac.in",
        "password": "password123"
    })
    print(res.json())
    assert res.status_code == 200
    assert res.json()['needs_password_change'] is True
    
    # 4. Change Password
    print("\nTesting Change Password...")
    res = student_session.post(f"{BASE_URL}/change-password", json={
        "new_password": "newpassword123"
    })
    print(res.json())
    assert res.status_code == 200
    
    # 5. Student Login with New Password
    print("\nTesting Student Login with New Password...")
    final_session = requests.Session()
    res = final_session.post(f"{BASE_URL}/login", json={
        "email": "teststudent1@nilgiricollege.ac.in",
        "password": "newpassword123"
    })
    print(res.json())
    assert res.status_code == 200
    assert 'needs_password_change' not in res.json() or res.json()['needs_password_change'] is False
    assert res.json()['role'] == 'student'

    print("\nVerification Successful!")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"\nVerification Failed: {e}")
