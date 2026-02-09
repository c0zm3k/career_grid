import pandas as pd
import os

def generate_template():
    # Define columns exactly as required by seed_from_excel.py
    columns = ['email', 'full_name', 'department', 'cgpa', 'passing_year', 'password']
    
    # Sample data
    data = [
        ['john.doe@nilgiricollege.ac.in', 'John Doe', 'Computer Science', 8.5, 2024, 'password123'],
        ['jane.smith@nilgiricollege.ac.in', 'Jane Smith', 'Arts & Media', 7.9, 2023, 'password123'],
        ['student.demo@nilgiricollege.ac.in', 'Demo Student', 'Commerce', 9.1, 2025, 'password123']
    ]
    
    df = pd.DataFrame(data, columns=columns)
    
    # Save to static/cdn
    output_path = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'cdn', 'student_template.xlsx')
    
    # Ensure directory exists (though cdn should already exist)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_excel(output_path, index=False)
    print(f"Template generated at: {output_path}")

if __name__ == "__main__":
    generate_template()
