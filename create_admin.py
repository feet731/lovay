from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    username = 'admin'
    password = 'admin123'  # Измените пароль в продакшене!
    if not User.query.filter_by(username=username).first():
        user = User(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(user)
        db.session.commit()
        print(f'Admin user {username} created successfully!')
    else:
        print('Admin user already exists!')