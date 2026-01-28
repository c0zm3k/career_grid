import requests

BASE_URL = "http://127.0.0.1:5000"

def verify_student_edit():
    session = requests.Session()
    
    print("1. Logging in as Admin...")
    session.post(f"{BASE_URL}/login", json={"email": "admin@nilgiricollege.ac.in", "password": "admin123"})
    
    # Get a student to edit
    print("2. Fetching student list...")
    dash_html = session.get(f"{BASE_URL}/admin/dashboard").text
    if "Enrolled Students" not in dash_html:
        print("FAIL: Student list not found in dashboard")
        return

    # Let's find a profile ID from the DB directly for precision
    import sqlite3
    conn = sqlite3.connect('e:/career_grid/instance/career_grid.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, department, cgpa FROM student_profile LIMIT 1")
    student = cursor.fetchone()
    conn.close()
    
    if not student:
        print("FAIL: No student profiles found in DB")
        return
        
    profile_id, name, old_dept, old_cgpa = student
    print(f"   Editing student: {name} (ID: {profile_id})")
    print(f"   Current: Dept={old_dept}, CGPA={old_cgpa}")
    
    print("3. Attempting to update student profile via API...")
    new_dept = "Updated Dept " + str(old_dept)
    new_cgpa = 9.99
    payload = {
        "department": new_dept,
        "cgpa": new_cgpa
    }
    update_res = session.post(f"{BASE_URL}/api/admin/student/update/{profile_id}", json=payload)
    if not update_res.ok:
        print(f"FAILED UPDATE: {update_res.text}")
        return

    print("4. Verifying state after update...")
    # Refresh DB connection to see changes
    conn = sqlite3.connect('e:/career_grid/instance/career_grid.db')
    cursor = conn.cursor()
    cursor.execute("SELECT department, cgpa FROM student_profile WHERE id=?", (profile_id,))
    updated = cursor.fetchone()
    conn.close()
    
    dept_match = updated[0] == new_dept
    cgpa_match = abs(updated[1] - new_cgpa) < 0.01
    
    print(f"   Dept updated: {dept_match} (New value: {updated[0]})")
    print(f"   CGPA updated: {cgpa_match} (New value: {updated[1]})")
    
    if dept_match and cgpa_match:
        print("\nPASS: Admin successfully updated student credentials.")
    else:
        print("\nFAIL: Student update failed.")

if __name__ == "__main__":
    verify_student_edit()
