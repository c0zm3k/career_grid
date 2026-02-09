from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from . import db
from .models import User, Job, StudentProfile, Application, ActivityLog
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

# Create a Blueprint for main routes
main = Blueprint('main', __name__)

@main.route('/')
def home_page():
    return render_template('index.html')

@main.route('/login')
def login_page():
    return render_template('login.html')

@main.route('/about')
def about_page():
    return render_template('about.html')

@main.route('/jobs-page') # Renamed list route to avoid conflict with API
def jobs_page():
    return render_template('jobs.html')

@main.route('/portfolio-page')
@login_required
def portfolio_page():
    if current_user.role != 'student':
        return "Access restricted to students", 403
    return render_template('portfolio.html')

@main.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'admin') # Default to admin for self-signup
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    
    # Self-signup is for Admins only and they need approval
    new_user = User(
        email=email, 
        password=hashed_pw, 
        role='admin', 
        is_approved=False, # Requires Super Admin approval
        needs_password_change=False # They set their own password during signup
    )
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Signup successful! Please wait for Super Admin approval."})

@main.route('/api')
def api_info():
    return jsonify({
        "message": "Welcome to the Career Grid API",
        "endpoints": {
            "signup": "/signup [POST]",
            "login": "/login [POST]",
            "jobs": "/jobs [GET, POST]",
            "portfolio": "/portfolio [GET, POST]",
            "chatbot": "/chatbot [POST]"
        }
    })

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'superadmin']:
            if request.is_json:
                return jsonify({"error": "Admin access required"}), 403
            return redirect(url_for('main.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'superadmin':
            if request.is_json:
                return jsonify({"error": "Super Admin access required"}), 403
            return redirect(url_for('main.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def password_change_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.needs_password_change:
            if request.endpoint != 'main.change_password' and request.endpoint != 'main.logout':
                return jsonify({"redirect": "/change-password", "error": "Password change required"}), 403 if request.is_json else render_template('change_password.html')
        return f(*args, **kwargs)
    return decorated_function

# --- MODULE 1: LOGIN ---
@main.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and check_password_hash(user.password, data.get('password')):
        if not user.is_approved:
            return jsonify({"error": "Your account is pending Super Admin approval."}), 403
            
        login_user(user)
        if user.needs_password_change:
            return jsonify({"message": "Password change required", "redirect": "/change-password", "needs_password_change": True})
        
        # Redirect based on role
        redirect_url = '/student/dashboard' if user.role == 'student' else '/admin/dashboard'
        return jsonify({"message": "Login successful", "role": user.role, "redirect": redirect_url})
    return jsonify({"error": "Invalid credentials"}), 401

@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        data = request.json
        new_password = data.get('new_password')
        if not new_password or len(new_password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        
        current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        current_user.needs_password_change = False
        db.session.commit()
        return jsonify({"message": "Password updated successfully!"})
    
    return render_template('change_password.html')

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})

# --- MODULE 2: STUDENT PORTFOLIO ---
@main.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    if current_user.role != 'student':
        return jsonify({"error": "Access restricted to students"}), 403
    if request.method == 'POST':
        data = request.json
        profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = StudentProfile(user_id=current_user.id)
        
        # Official info is locked for students
        # profile.full_name = data.get('full_name')
        # profile.cgpa = data.get('cgpa')
        # profile.department = data.get('department')
        
        profile.skills = data.get('skills')
        profile.resume_link = data.get('resume_link')
        
        db.session.add(profile)
        db.session.commit()
        return jsonify({"message": "Portfolio updated!"})
    
    profile = current_user.profile
    if profile:
        return jsonify({
            "full_name": profile.full_name,
            "cgpa": profile.cgpa,
            "passing_year": profile.passing_year,
            "skills": profile.skills,
            "department": profile.department,
            "resume_link": profile.resume_link
        })
    return jsonify({"message": "Profile empty"}), 404

# --- MODULE 3: JOB & INTERNSHIP ---
@main.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    output = []
    for job in jobs:
        output.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "min_cgpa": job.min_cgpa,
            "deadline": job.deadline.isoformat()
        })
    return jsonify({"jobs": output})

@main.route('/jobs', methods=['POST'])
@login_required
@admin_required
def add_job():
    if current_user.role != 'admin':
        return jsonify({"error": "Only standard Admins can post jobs"}), 403
    data = request.json
    try:
        deadline = datetime.fromisoformat(data.get('deadline'))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid deadline format. Use ISO format (YYYY-MM-DD)."}), 400

    new_job = Job(
        title=data.get('title'),
        company=data.get('company'),
        description=data.get('description'),
        min_cgpa=data.get('min_cgpa', 0.0),
        deadline=deadline
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({"message": "Job posted successfully!", "job_id": new_job.id})

@main.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Check eligibility
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile or (profile.cgpa or 0) < job.min_cgpa:
        return jsonify({"error": "You do not meet the minimum CGPA requirement for this job."}), 403

    # Check if already applied
    existing_app = Application.query.filter_by(job_id=job_id, student_id=current_user.id).first()
    if existing_app:
        return jsonify({"error": "You have already applied for this job."}), 400

    new_application = Application(job_id=job_id, student_id=current_user.id)
    db.session.add(new_application)
    db.session.commit()
    
    # Placeholder for notification
    print(f"Notification sent to {current_user.email}") 
    
    return jsonify({"message": "Application submitted successfully!"})

# --- MODULE 5: DASHBOARDS & ADMIN TOOLS ---
@main.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    stats = {
        "total_students": User.query.filter_by(role='student').count(),
        "total_jobs": Job.query.count(),
        "total_applications": Application.query.count()
    }
    
    # Extra data based on role
    active_admins = []
    pending_admins = []
    students = []
    
    if current_user.role == 'superadmin':
        active_admins = User.query.filter_by(role='admin', is_approved=True).all()
        pending_admins = User.query.filter_by(role='admin', is_approved=False).all()
    elif current_user.role == 'admin':
        students = User.query.filter_by(role='student').limit(50).all()
        
    activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(15).all()
        
    return render_template('admin_dashboard.html', stats=stats, active_admins=active_admins, pending_admins=pending_admins, students=students, activities=activities)

@main.route('/api/admin/create', methods=['POST'])
@login_required
@superadmin_required
def create_admin_api():
    data = request.json
    email = data.get('email')
    password = data.get('password', 'admin123')
    
    if not email:
        return jsonify({"error": "Email required"}), 400
        
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
        
    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    new_admin = User(email=email, password=hashed_pw, role='admin', needs_password_change=False, is_approved=True)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin account created successfully!"})

@main.route('/api/admin/approve/<int:admin_id>', methods=['POST'])
@login_required
@superadmin_required
def approve_admin(admin_id):
    admin = User.query.get_or_404(admin_id)
    admin.is_approved = True
    db.session.commit()
    return jsonify({"message": "Admin approved successfully"})

@main.route('/api/admin/update/<int:admin_id>', methods=['POST'])
@login_required
@superadmin_required
def update_admin(admin_id):
    admin = User.query.get_or_404(admin_id)
    data = request.json
    
    if 'email' in data:
        email = data['email']
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != admin.id:
            return jsonify({"error": "Email already in use"}), 400
        admin.email = email
    if 'password' in data and data['password']:
        admin.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        admin.needs_password_change = False # Super admin reset it
        
    db.session.commit()
    return jsonify({"message": "Admin updated successfully"})

@main.route('/api/admin/delete/<int:admin_id>', methods=['POST'])
@login_required
@superadmin_required
def delete_admin_api(admin_id):
    admin = User.query.get_or_404(admin_id)
    if admin.role != 'admin':
        return jsonify({"error": "Cannot delete this user type"}), 403
        
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin account deleted successfully!"})

@main.route('/student/dashboard')
@login_required
def student_dashboard():
    # Pass student stats/recent activities
    profile = current_user.profile
    apps = Application.query.filter_by(student_id=current_user.id).all()
    return render_template('student_dashboard.html', profile=profile, applications=apps)

@main.route('/admin/upload-students', methods=['POST'])
@login_required
@admin_required
def upload_students():
    if current_user.role != 'admin':
        return jsonify({"error": "Only standard Admins can upload student data"}), 403
    import pandas as pd
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        try:
            df = pd.read_excel(file)
            required_cols = ['email', 'full_name', 'department', 'cgpa', 'passing_year', 'password']
            if not all(col in df.columns for col in required_cols):
                return jsonify({"error": f"Excel must contain columns: {', '.join(required_cols)}"}), 400
            
            for _, row in df.iterrows():
                email = str(row['email']).strip()
                user = User.query.filter_by(email=email).first()
                if not user:
                    # Create new user
                    temp_pwd = str(row['password']).strip()
                    hashed_pw = generate_password_hash(temp_pwd, method='pbkdf2:sha256')
                    new_user = User(email=email, password=hashed_pw, role='student', needs_password_change=True)
                    db.session.add(new_user)
                    db.session.flush() # Get user id
                    
                    new_profile = StudentProfile(
                        user_id=new_user.id,
                        full_name=row['full_name'],
                        department=row['department'],
                        cgpa=float(row['cgpa']),
                        passing_year=int(row['passing_year']) if 'passing_year' in row else None
                    )
                    db.session.add(new_profile)
                else:
                    # Update existing user profile if it's a student
                    if user.role == 'student':
                        if not user.profile:
                            user.profile = StudentProfile(user_id=user.id)
                        user.profile.full_name = row['full_name']
                        user.profile.department = row['department']
                        user.profile.cgpa = float(row['cgpa'])
                        user.profile.passing_year = int(row['passing_year']) if 'passing_year' in row else user.profile.passing_year
            
            db.session.commit()
            
            # Log Activity
            upload_log = ActivityLog(
                user_id=current_user.id,
                action='Excel Upload',
                details=f"Uploaded/Updated {len(df)} students via Excel."
            )
            db.session.add(upload_log)
            db.session.commit()

            return jsonify({"message": "Students uploaded/updated successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid file format"}), 400

@main.route('/api/admin/student/update/<int:profile_id>', methods=['POST'])
@login_required
@admin_required
def update_student_profile(profile_id):
    profile = StudentProfile.query.get_or_404(profile_id)
    data = request.json
    
    if 'department' in data:
        profile.department = data['department']
    if 'cgpa' in data:
        try:
            profile.cgpa = float(data['cgpa'])
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid CGPA value"}), 400
    if 'passing_year' in data:
        try:
            profile.passing_year = int(data['passing_year'])
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid Passing Year value"}), 400
            
    db.session.commit()
    return jsonify({"message": "Student profile updated successfully"})

@main.route('/api/admin/student/create-manual', methods=['POST'])
@login_required
@admin_required
def create_student_manual():
    data = request.json
    email = data.get('email', '').strip()
    full_name = data.get('full_name', '').strip()
    department = data.get('department', '').strip()
    cgpa = data.get('cgpa', 0.0)
    passing_year = data.get('passing_year')
    password = data.get('password', 'password123').strip()

    if not email or not full_name:
        return jsonify({"error": "Email and Full Name are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    try:
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_pw, role='student', needs_password_change=True, is_approved=True)
        db.session.add(new_user)
        db.session.flush()

        new_profile = StudentProfile(
            user_id=new_user.id,
            full_name=full_name,
            department=department,
            cgpa=float(cgpa),
            passing_year=int(passing_year) if passing_year else None
        )
        db.session.add(new_profile)

        # Log Activity
        entry_log = ActivityLog(
            user_id=current_user.id,
            action='Manual Student Entry',
            details=f"Added student: {full_name} ({email})"
        )
        db.session.add(entry_log)
        
        db.session.commit()
        return jsonify({"message": "Student added successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
