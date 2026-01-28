from app import db, create_app
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    print("ID | Email | Role | Approved | Needs Pass Change")
    print("-" * 60)
    for u in users:
        print(f"{u.id} | {u.email} | {u.role} | {u.is_approved} | {u.needs_password_change}")
