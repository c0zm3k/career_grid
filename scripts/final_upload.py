import requests

BASE_URL = "http://127.0.0.1:5000"

def upload():
    session = requests.Session()
    session.post(f"{BASE_URL}/login", json={"email": "superadmin@nilgiricollege.ac.in", "password": "superadmin123"})
    session.post(f"{BASE_URL}/api/admin/create", json={"email": "admin@nilgiricollege.ac.in", "password": "admin123"})
    session.post(f"{BASE_URL}/logout")
    
    session.post(f"{BASE_URL}/login", json={"email": "admin@nilgiricollege.ac.in", "password": "admin123"})
    with open("test_students.xlsx", "rb") as f:
        session.post(f"{BASE_URL}/admin/upload-students", files={"file": f})

if __name__ == "__main__":
    upload()
