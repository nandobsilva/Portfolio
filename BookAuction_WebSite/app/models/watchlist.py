from app import db
from datetime import datetime


class Watchlist(db.Model):
    # Database table user
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    status = db.Column(db.Boolean, index=True, nullable=True, unique=False, default=True)
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    # Functions
    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return f"id: {self.id}, create_at: {self.created_at}, user_id: {self.user_id}, book_id: {self.book_id}, status: {self.status}"

    def get_books(self):
        return 0

    def add_book(self):
        result = Watchlist.query.filter_by(user_id=self.user_id, book_id=self.book_id).first()
        # if book is not in the user watchlist return 1
        if result is None:
            item = Watchlist(self.user_id, self.book_id)
            db.session.add(item)
            db.session.commit()
            return 1
        elif result.status is False:
            #If book is in the user watch list but status = False (book not visible)
            item = Watchlist.query.filter_by(user_id=self.user_id, book_id=self.book_id).first()
            item.status = True
            db.session.commit()
            return 2
        else:
            return 0

    @staticmethod
    def delete_book(item_id: int):
        item = Watchlist.query.filter_by(id=item_id).first()
        item.status = False
        db.session.commit()



