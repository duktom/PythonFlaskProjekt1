from extensions import db, bcrypt
from database.models import User


def create_user(username, password):
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def check_user_password(user, password):
    if not user:
        return False
    return bcrypt.check_password_hash(user.password, password)
