import requests

BASE_URL = "http://127.0.0.1:5000"

def verify_visibility():
    session = requests.Session()
    
    print("1. Verifying Super Admin View...")
    session.post(f"{BASE_URL}/login", json={"email": "superadmin@nilgiricollege.ac.in", "password": "superadmin123"})
    dash_super = session.get(f"{BASE_URL}/admin/dashboard").text
    
    has_admins = "Active Administrators" in dash_super
    has_students = "Enrolled Students" in dash_super
    
    print(f"   - Has Admins section: {has_admins}")
    print(f"   - Has Students section: {has_students}")
    
    if has_admins and not has_students:
        print("   PASS: Super Admin view is correct.")
    else:
        print("   FAIL: Super Admin view incorrect.")
        
    session.post(f"{BASE_URL}/logout")
    
    print("\n2. Verifying Admin View...")
    session.post(f"{BASE_URL}/login", json={"email": "admin@nilgiricollege.ac.in", "password": "admin123"})
    dash_admin = session.get(f"{BASE_URL}/admin/dashboard").text
    
    has_admins = "Active Administrators" in dash_admin
    has_students = "Enrolled Students" in dash_admin
    
    print(f"   - Has Admins section: {has_admins}")
    print(f"   - Has Students section: {has_students}")
    
    if not has_admins and has_students:
        print("   PASS: Admin view is correct.")
    else:
        print("   FAIL: Admin view incorrect.")

if __name__ == "__main__":
    verify_visibility()
