from app import db
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model, UserMixin):
    # Database table users
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True, nullable=False, unique=False)
    phone = db.Column(db.String(30), index=True, nullable=False, unique=False)
    address = db.Column(db.String(30), index=True, nullable=False, unique=False)
    email = db.Column(db.String(30), index=True, nullable=False, unique=True)
    password = db.Column(db.String(400), nullable=False)
    # Virtual database foreignkey reference
    book = db.relationship('Book', backref='user')
    watchlist = db.relationship('Watchlist', backref='user')
    bid = db.relationship('Bid', backref='user')
    review = db.relationship('Review', backref='user')

    # Functions
    def __init__(self, user_name: str, user_email: str, user_password: str, user_phone: str, user_address: str):
        self.id = None
        self.name = user_name
        self.email = user_email
        self.password = user_password
        self.phone = user_phone
        self.address = user_address

    def __repr__(self):
        return f"id:{self.id}, name: {self.name}, email: {self.email}"

    def register(self):
        result = User.query.filter_by(email=self.email).first()
        # if email is not in the database add it
        if result is None:
            user = User(self.name, self.email, self.password, self.phone, self.address)
            db.session.add(user)
            db.session.commit()
            return 1
        else:
            return 0

    @staticmethod
    def login(email: str, password: str):
        user = User.query.filter_by(email=email).first()
        # If user does not exist in the database
        if user is None:
            return 0
        # If user exist in the database
        else:
            pwd_validation = check_password_hash(user.password, password)
            # If user exist but password is incorrect
            if not pwd_validation:
                return 0
            # User exist and password is correct
            return user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
