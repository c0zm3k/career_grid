# 🎓 Career Grid
A modern, sleek Placement Management System built with **Flask** and **SQLAlchemy**, tailored for **Nilgiri College**.

Career Grid streamlines the placement process by providing distinct portals for students and recruiters. It features a robust Role-Based Access Control (RBAC) system to ensure secure interactions and academic-centric portfolio management.

## ✨ Key Features

### 🎨 User Interface
- **Premium Design**: A high-end aesthetic matching the Nilgiri College brand.
- **Role-Based Dashboards**: Tailored experiences for Students and Admins based on their specific activities.
- **Mobile First**: Fully responsive layout optimized for all device sizes.
- **Micro-interactions**: Smooth transitions and hover effects for an engaging experience.

### 🔐 Access Control
- **Institutional Enrollment Only**: Public signup is disabled; students are added via controlled administrative flows.
- **Secure First Login**: Mandatory password change for all initial student accounts to ensure individual security.
- **Enhanced RBAC**: Restricted page access using bespoke decorators (`@admin_required`, `@superadmin_required`).
- **Secure Sessions**: Powered by `Flask-Login` with encrypted password hashing.

### 📚 Modules
- **Admin Management**: Bulk student enrollment via Excel (.xlsx) upload.
- **Job & Internship Board**: Centralized repository for all career opportunities.
- **Student Portfolio**: Professional academic records including CGPA and skill tracking.

## 🛠️ Tech Stack
- **Backend**: Python, Flask, Jinja2
- **Data Processing**: Pandas, OpenPyxl (for Excel automation)
- **Database**: SQLite (Dev), SQLAlchemy (ORM)
- **Frontend**: Vanilla JavaScript, CSS3 (Modern Flexbox/Grid)
- **Security**: PBKDF2 Password Hashing

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python Package Installer)

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd career_grid
   ```

2. **Install Dependencies**
   ```bash
   py -m pip install flask flask-sqlalchemy flask-login requests pandas openpyxl
   ```

3. **Initialize Database & Seed Admin**
   ```bash
   py scripts/reset_db.py
   ```
   *Note: This script initializes the schema and creates the Super Admin account.*

4. **Run the Application**
   ```bash
   py run.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

## ☁️ Deployment (Render)

1. **Create a Web Service**: Connect your GitHub repository to Render.
2. **Environment**: Select `Python` as the environment.
3. **Build Command**: 
   ```bash
   pip install -r requirements.txt
   ```
4. **Start Command**:
   ```bash
   gunicorn app:app
   ```
5. **Database**: Render uses an ephemeral filesystem. For production, consider connecting to a Managed PostgreSQL instance or using a persistent disk if you want to keep the SQLite `instance/` folder.

## 👤 User Directory & Credentials

### 🌟 Admin Access
| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@nilgiricollege.ac.in` | `Nilgiri@Admin2026` | Full System Control & User Management |
| **Placement Admin** | `admin1@nilgiricollege.ac.in` | `password123` | Student Enrollment & Job Posting |

### 📥 Student Enrollment Flow
1. **Admin** uploads a student master list (Excel) via the Admin Dashboard.
2. **Students** receive a temporary password (`password123`).
3. **On First Login**, students are redirected to set a unique personal password.

## 📂 Project Structure
```text
career_grid/
├── app/                  # Flask Application & Core Logic
│   ├── static/           # CSS, JS, and Images
│   └── templates/        # Jinja2 HTML Templates
├── scripts/              # Utility, Seeding, and Verification scripts
├── instance/             # Local database storage (SQLite)
├── .gitignore            # Git exclusion rules
├── config.py             # App configuration
├── login_credentials.txt # Registry of test accounts
├── README.md             # Project Documentation
├── requirements.txt      # Production dependencies
└── run.py                # Application entry point (Local Dev)
```
