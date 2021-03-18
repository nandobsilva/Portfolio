from app import db
from datetime import datetime


class Book(db.Model):
    # Database table books
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True, nullable=False, unique=False)
    author = db.Column(db.String(30), index=True, nullable=False, unique=False)
    description = db.Column(db.String(400), index=True, nullable=True, unique=False)
    category = db.Column(db.String(30), index=True, nullable=False, unique=False)
    isbn = db.Column(db.String(30), index=True, nullable=True, unique=False)
    start_bid_amount = db.Column(db.Float, nullable=False, unique=False)
    bid_status = db.Column(db.String(20), index=True, nullable=True, unique=False, default="Open")
    image_url = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Virtual database foreignkey reference
    watchlist = db.relationship('Watchlist', backref='book')
    bid = db.relationship('Bid', backref='book')
    review = db.relationship('Review', backref='book')

    # Functions
    def __init__(self):
        self.title = None
        self.author = None
        self.description = None
        self.category = None
        self.isbn = None
        self.start_bid_amount = None
        self.image_url = None
        self.bid_status = None

    def __repr__(self):
        return f"id: {self.id}, title: {self.title}, author: {self.author}," \
               f"description:{self.description},category:{self.category},isbn:{self.isbn}, " \
               f"start_bid_amount: {self.start_bid_amount}, bid_status:{self.bid_status}, " \
               f"image_url:{self.image_url}, user_id: {self.user_id}, created_at: {self.created_at}"

    def addBook(self):
        # add book in the database
        db.session.add(self)
        db.session.commit()


    def getBookDetail(self):
        return 0

    @staticmethod
    def updateBookStatus(book_id: int, status: str):
        book = Book.query.filter_by(id=book_id).first()
        if status == "Open" or status == "Inactive" or status == "Closed":
            book.bid_status = status
            db.session.add(book)
            db.session.commit()
            return 1
        else:
            return 0


