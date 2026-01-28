import requests

BASE_URL = "http://127.0.0.1:5000"

def verify_locking():
    session = requests.Session()
    
    print("1. Logging in as student (rahul.nair@nilgiricollege.ac.in) with reset password...")
    login_res = session.post(f"{BASE_URL}/login", json={"email": "rahul.nair@nilgiricollege.ac.in", "password": "p1"})
    if not login_res.ok:
        print(f"FAILED LOGIN: {login_res.text}")
        return

    print("2. Fetching current portfolio state...")
    original_res = session.get(f"{BASE_URL}/portfolio")
    original = original_res.json()
    print(f"   Name: {original.get('full_name')}, CGPA: {original.get('cgpa')}")
    
    print("3. Attempting to update locked fields via API...")
    payload = {
        "full_name": "HACKER NAME",
        "department": "HACKER DEPT",
        "cgpa": 10.0,
        "skills": "Verified Skills Update",
        "resume_link": "http://verified-rahul.com"
    }
    update_res = session.post(f"{BASE_URL}/portfolio", json=payload)
    
    print("4. Verifying state after update attempt...")
    updated = session.get(f"{BASE_URL}/portfolio").json()
    
    name_locked = updated.get('full_name') == original.get('full_name')
    dept_locked = updated.get('department') == original.get('department')
    cgpa_locked = updated.get('cgpa') == original.get('cgpa')
    skills_updated = updated.get('skills') == "Verified Skills Update"
    
    print(f"   Name locked: {name_locked} (Value: {updated.get('full_name')})")
    print(f"   Dept locked: {dept_locked} (Value: {updated.get('department')})")
    print(f"   CGPA locked: {cgpa_locked} (Value: {updated.get('cgpa')})")
    print(f"   Skills updated: {skills_updated}")
    
    if name_locked and dept_locked and cgpa_locked and skills_updated:
        print("\nPASS: Critical fields are strictly locked in backend. Editable fields updated.")
    else:
        print("\nFAIL: Field locking protection failed.")

if __name__ == "__main__":
    verify_locking()
