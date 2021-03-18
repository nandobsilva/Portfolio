from flask import Blueprint, render_template, request, session, redirect, abort, url_for
from flask_login import login_required, current_user
from app.models.watchlist import Watchlist
from app.functions import getTop5, getHighestBid, getBook
from app.models.bid import Bid


watchlist_blueprint = Blueprint('watchlist', __name__, url_prefix='/watchlist')

log_in_message = "User must log in to access this page."
watchlist_message_01 = "You can not add this item in your watchlist because you are the owner of this book"
watchlist_message_02 = "This book is already in your watchlist"
watchlist_message_03 = "The book was successfully added in your watchlist"


@watchlist_blueprint.route('/')
@login_required
def watchlist():
    top5 = getTop5()
    watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()
    # Format watchlist.created_at date variable
    for item in watchlist:
        book = getBook(item.book_id)
        item.date_formatted = item.created_at.strftime('%d/%m/%Y')
        item.start_bid_amount_formatted = '{:.2f}'.format(book.start_bid_amount)
        item.highest_bid = getHighestBid(book.id)
        num_bids = 0
        bids = Bid.query.filter_by(book_id=book.id).order_by(Bid.bid_amount).all()
        for bid in bids:
            num_bids += 1
        item.num_bid = num_bids

    return render_template('watchlist/watchlist.html', watchlist=watchlist, top5=top5)


@watchlist_blueprint.route('/add/<book_user_id>/<book_id>/<next>', methods=['POST', 'GET'])
@login_required
def watchlist_add(book_user_id, book_id, next):
    # If book is owned by the user show  watchlist_message_01
    if str(current_user.id) == book_user_id:
        return redirect(url_for(next, book_id=book_id, message=watchlist_message_01))
    # If books is not in the user's watch list
    else:
        item = Watchlist(current_user.id, book_id)
        result = item.add_book()
        # If book is not in the user watchlist, add it.
        if result == 1:
            return redirect(url_for(next, book_id=book_id, message=watchlist_message_03))
        # If book is already in the user watchlist but is inactive, active it.
        elif result == 2:
            return redirect(url_for(next, book_id=book_id, message=watchlist_message_03))
        # If book is already in the user watchlist, show watchlist_message_02.
        else:
            return redirect(url_for(next, book_id=book_id, message=watchlist_message_02))


@watchlist_blueprint.route('/delete/<item_id>', methods=['POST', 'GET'])
@login_required
def watchlist_delete(item_id):
    Watchlist.delete_book(item_id)
    return redirect(url_for('watchlist.watchlist'))


@watchlist_blueprint.route('/add/<book_user_id>', methods=['POST', 'GET'])
@login_required
def watchlist_add_01(book_user_id):
    return render_template('watchlist/error.html', message=log_in_message)