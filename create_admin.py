from werkzeug.security import generate_password_hash

from app import app
from models import db, User

with app.app_context():

    admin = User(
        username="admin",
        password=generate_password_hash("admin123"),
        role="Admin"
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin Created")