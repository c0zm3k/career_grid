import requests

BASE_URL = "http://127.0.0.1:5000"

def verify_split_ui():
    session = requests.Session()
    
    print("1. Signing up a new Admin (Public flows)...")
    res = requests.post(f"{BASE_URL}/signup", json={
        "email": "pending.admin@nilgiricollege.ac.in",
        "password": "password123"
    })
    print(f"Signup Response: {res.json()}")

    print("\n2. Logging in as Super Admin...")
    session.post(f"{BASE_URL}/login", json={
        "email": "superadmin@nilgiricollege.ac.in",
        "password": "superadmin123"
    })
    
    print("\n3. Checking dashboard for Pending list...")
    res = session.get(f"{BASE_URL}/admin/dashboard")
    if "Pending Approvals" in res.text and "pending.admin@nilgiricollege.ac.in" in res.text:
        print("SUCCESS: Pending admin found in Pending list.")
    else:
        print("FAILED: Pending admin not found or list missing.")

    print("\n4. Approving the admin...")
    # Get ID from data if possible, but let's assume it's 2 (1 is superadmin)
    res = session.post(f"{BASE_URL}/api/admin/approve/2")
    print(f"Approval Response: {res.json()}")

    print("\n5. Checking dashboard for Active list...")
    res = session.get(f"{BASE_URL}/admin/dashboard")
    if "Active Administrators" in res.text and "pending.admin@nilgiricollege.ac.in" in res.text:
        print("SUCCESS: Admin moved to Active list.")
    else:
        print("FAILED: Admin not found in Active list.")

    print("\n6. Creating an Admin via Super Admin (Internal flow)...")
    res = session.post(f"{BASE_URL}/api/admin/create", json={
        "email": "auto.verified@nilgiricollege.ac.in",
        "password": "admin123"
    })
    print(f"Creation Response: {res.json()}")

    print("\n7. Verifying Auto-Verification...")
    res = session.get(f"{BASE_URL}/admin/dashboard")
    if "auto.verified@nilgiricollege.ac.in" in res.text and "Verified Active" in res.text:
         print("SUCCESS: Internal admin is auto-verified and in Active list.")
    else:
         print("FAILED: Internal admin not verified or missing.")

if __name__ == "__main__":
    verify_split_ui()
