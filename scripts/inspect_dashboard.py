import requests

BASE_URL = "http://127.0.0.1:5000"

def inspect_dashboard():
    session = requests.Session()
    session.post(f"{BASE_URL}/login", json={
        "email": "superadmin@nilgiricollege.ac.in",
        "password": "superadmin123"
    })
    
    res = session.get(f"{BASE_URL}/admin/dashboard")
    print(f"Response Status: {res.status_code}")
    
    with open("dashboard_dump.html", "w", encoding="utf-8") as f:
        f.write(res.text)
    
    print("\nSearch Results:")
    print(f"'Pending Approvals' in text: {'Pending Approvals' in res.text}")
    print(f"'Active Administrators' in text: {'Active Administrators' in res.text}")
    print(f"'auto.verified@nilgiricollege.ac.in' in text: {'auto.verified@nilgiricollege.ac.in' in res.text}")
    print(f"'Verified Active' in text: {'Verified Active' in res.text}")

if __name__ == "__main__":
    inspect_dashboard()
