from app import db
from datetime import datetime
from sqlalchemy.sql import func
from app.models.book import Book


class Bid(db.Model):
    # Database table user
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    bid_amount = db.Column(db.Float, nullable=False, unique=False)
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def __init__(self, bid_amount: float, user_id: int, book_id: int):
        self.bid_amount = bid_amount
        self.user_id = user_id
        self.book_id = book_id


    def __repr__(self):
        return f"id: {self.id}, created_at: {self.created_at}, bid_amount: {self.bid_amount}, user_id: {self.user_id}, book_id: {self.book_id}"

    def add_bid(self):
        bids = Bid.query.filter_by(book_id=self.book_id).order_by(Bid.bid_amount).all()
        book = Book.query.filter_by(id=self.book_id).first()
        # Find highest bid amount
        highest = book.start_bid_amount
        # If book has bids
        if bids:
            for bid in bids:
                if bid.bid_amount > highest:
                    highest = bid.bid_amount
            # Check if the bid placed by the user is bigger than the highest bid_amount placed for the book
            if int(self.bid_amount) > int(highest):
                bid = Bid(self.bid_amount, self.user_id, self.book_id)
                db.session.add(bid)
                db.session.commit()
                return True
            else:
                return int(highest)
        # If book has no bids
        else:
            if float(self.bid_amount) > float(book.start_bid_amount):
                bid = Bid(self.bid_amount, self.user_id, self.book_id)
                db.session.add(bid)
                db.session.commit()
                return True
            else:
                return False


    def get_bids(self):
        return 0

    def delete_book(self):
        return 0