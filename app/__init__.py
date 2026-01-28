from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from .routes import main
    app.register_blueprint(main)
    
    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    with app.app_context():
        db.create_all()  # Create tables for Users, Jobs, etc.
        
        # Ensure Super Admin exists (Crucial for Cloud Deployment like Render)
        admin_email = 'admin@nilgiricollege.ac.in'
        admin_user = User.query.filter_by(email=admin_email, role='superadmin').first()
        if not admin_user:
            print(f"Creating default Super Admin: {admin_email}")
            hashed_pw = generate_password_hash('Nilgiri@Admin2026', method='pbkdf2:sha256')
            admin = User(
                email=admin_email, 
                password=hashed_pw, 
                role='superadmin', 
                needs_password_change=False, 
                is_approved=True
            )
            db.session.add(admin)
            db.session.commit()
        
    return app

app = create_app()
