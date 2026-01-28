import requests
import re

BASE_URL = "http://127.0.0.1:5000"

def verify_robust():
    session = requests.Session()
    
    print("1. Admin Signup...")
    session.post(f"{BASE_URL}/signup", json={"email": "p1@nilgiri.in", "password": "p"})
    
    print("2. Super Admin Login...")
    session.post(f"{BASE_URL}/login", json={"email": "superadmin@nilgiricollege.ac.in", "password": "superadmin123"})
    
    print("3. Checking Pending list...")
    dash = session.get(f"{BASE_URL}/admin/dashboard").text
    if "Pending Approvals" in dash and "p1@nilgiri.in" in dash:
        print("PASS: Pending admin visible.")
    else:
        print("FAIL: Pending admin missing or section missing.")

    print("4. Approving...")
    session.post(f"{BASE_URL}/api/admin/approve/2")
    
    print("5. Internal Create...")
    session.post(f"{BASE_URL}/api/admin/create", json={"email": "a1@nilgiri.in", "password": "p"})
    
    print("6. Checking Active list...")
    dash = session.get(f"{BASE_URL}/admin/dashboard").text
    if "Active Administrators" in dash:
        print("PASS: Active section visible.")
        if "p1@nilgiri.in" in dash and "a1@nilgiri.in" in dash:
            print("PASS: Both admins in active list.")
        else:
            print(f"FAIL: Missing admins. (p1: {'p1@nilgiri.in' in dash}, a1: {'a1@nilgiri.in' in dash})")
        
        # Check for Verified Active badge (ignoring whitespace/newlines)
        if re.search(r"Verified\s+Active", dash):
             print("PASS: Verified Active badge found.")
        else:
             print("FAIL: Badge not found.")
    else:
        print("FAIL: Active section missing.")

if __name__ == "__main__":
    verify_robust()
