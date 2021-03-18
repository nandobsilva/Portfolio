from app.models.book import Book
from app.models.bid import Bid
from datetime import datetime
from app import db
import os

def dateToString():
    now = datetime.now()
    day = now.strftime('%d')
    month = now.strftime('%m')
    year = now.strftime('%Y')
    hour = now.strftime('%H')
    minutes = now.strftime('%M')
    seconds = now.strftime('%S')
    timestamp = now.strftime('%f')
    date = day+"_"+month+"_"+year+"_"+hour+"_"+minutes+"_"+seconds+"_"+timestamp
    return date

def appLocalPath():
    BASE_PATH = os.path.dirname(__file__)
    return BASE_PATH

def getTop5():
    book_bids_count = db.session.query(db.func.count(Bid.book_id), Book.id).outerjoin(Bid, Book.id == Bid.book_id).group_by(Book.id).all()
    new_list = []
    # Select just book with bids
    for bid in book_bids_count:
        if bid[0] > 0:
            new_list.append(bid)
    new_list.sort(reverse=True)
    # Select top 5 book with bids
    top5 = []
    if len(new_list) < 5:
        for x in range(0, len(new_list)):
            book = Book.query.filter_by(id=new_list[x][1]).first()
            book.bids = new_list[x][0]
            top5.append(book)
    else:
        for x in range(0, 5):
            book = Book.query.filter_by(id=new_list[x][1]).first()
            book.bids = new_list[x][0]
            top5.append(book)
    return top5

def getHighestBid(book_id: int):
    bids = Bid.query.filter_by(book_id=book_id).order_by(Bid.bid_amount).all()
    highest_bid = 0
    for bid in bids:
        if float(bid.bid_amount) > float(highest_bid):
            highest_bid = bid.bid_amount
    highest_bid = '{:.2f}'.format(highest_bid)
    return highest_bid

def getBook(book_id: int):
    book = Book.query.filter_by(id=book_id).first()
    return book