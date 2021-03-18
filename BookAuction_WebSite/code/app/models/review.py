from app import db
from datetime import datetime


class Review(db.Model):
    # Database table user
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(500), index=True, nullable=True, unique=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def __init__(self, user_id: int, book_id: int, review: str):
        self.review = review
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return f"id {self.id}, review: {self.review}, user_id: {self.user_id}, book_id: {self.book_id}, created_at: {self.created_at}"

    def add_review(self):
        review = Review(self.user_id, self.book_id, self.review)
        db.session.add(review)
        db.session.commit()
        return 1

