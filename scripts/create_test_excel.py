import pandas as pd

data = {
    'email': [
        'rahul.nair@nilgiricollege.ac.in', 'priya.sharma@nilgiricollege.ac.in', 'anish.v@nilgiricollege.ac.in',
        'sneha.k@nilgiricollege.ac.in', 'karthik.r@nilgiricollege.ac.in', 'meera.j@nilgiricollege.ac.in',
        'arjun.das@nilgiricollege.ac.in', 'anjali.m@nilgiricollege.ac.in', 'vikram.s@nilgiricollege.ac.in',
        'deepthy.p@nilgiricollege.ac.in', 'rohan.b@nilgiricollege.ac.in', 'swetha.v@nilgiricollege.ac.in',
        'gautam.k@nilgiricollege.ac.in', 'neha.r@nilgiricollege.ac.in', 'manoj.p@nilgiricollege.ac.in',
        'kavya.s@nilgiricollege.ac.in', 'akshay.t@nilgiricollege.ac.in', 'divya.m@nilgiricollege.ac.in',
        'siddharth.n@nilgiricollege.ac.in', 'amrita.b@nilgiricollege.ac.in', 'varun.g@nilgiricollege.ac.in',
        'shilpa.r@nilgiricollege.ac.in', 'abhinav.j@nilgiricollege.ac.in', 'pooja.v@nilgiricollege.ac.in',
        'vishnu.k@nilgiricollege.ac.in', 'lekshmi.s@nilgiricollege.ac.in', 'sanjay.m@nilgiricollege.ac.in',
        'revathy.p@nilgiricollege.ac.in', 'midhun.r@nilgiricollege.ac.in', 'arya.k@nilgiricollege.ac.in'
    ],
    'full_name': [
        'Rahul Nair', 'Priya Sharma', 'Anish Varma', 'Sneha Kapoor', 'Karthik Raja',
        'Meera Joseph', 'Arjun Das', 'Anjali Menon', 'Vikram Singh', 'Deepthy Pillai',
        'Rohan Bhaskar', 'Swetha Venkat', 'Gautam Krishna', 'Neha Reddy', 'Manoj Prabhu',
        'Kavya Suresh', 'Akshay Thampi', 'Divya Mohan', 'Siddharth Narayan', 'Amrita Bose',
        'Varun Gupta', 'Shilpa Roy', 'Abhinav Joshi', 'Pooja Verma', 'Vishnu Kumar',
        'Lekshmi S Nair', 'Sanjay Mahesh', 'Revathy P Babu', 'Midhun Rajesh', 'Arya Krishnan'
    ],
    'department': [
        'Computer Science', 'Commerce', 'Computer Science', 'Psychology', 'Commerce',
        'English', 'Computer Science', 'Commerce', 'Physics', 'Chemistry',
        'Computer Science', 'Commerce', 'Management', 'Psychology', 'Computer Science',
        'Commerce', 'Mathematics', 'English', 'Computer Science', 'Commerce',
        'Management', 'Physics', 'Computer Science', 'Commerce', 'Chemistry',
        'English', 'Computer Science', 'Commerce', 'Mathematics', 'Psychology'
    ],
    'cgpa': [
        8.2, 7.5, 9.1, 8.8, 6.9, 8.0, 7.2, 8.5, 9.3, 7.7,
        8.6, 7.9, 8.1, 8.4, 7.0, 8.3, 9.0, 7.6, 8.7, 8.2,
        7.4, 8.9, 9.2, 7.3, 8.1, 7.8, 8.5, 8.0, 7.9, 8.6
    ],
    'password': ['temp123'] * 30
}

df = pd.DataFrame(data)
df.to_excel('test_students.xlsx', index=False)
print("test_students.xlsx created with 30 realistic entries!")
