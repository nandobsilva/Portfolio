from flask import Blueprint, render_template, request, session, redirect, abort, url_for
from flask_login import login_required, current_user
from app.models.book import Book
from app.models.bid import Bid

bid_blueprint = Blueprint('bid', __name__, url_prefix='/bid')

bid_message_01 = "You can not add a bid because you are the owner of this book "
bid_message_02 = "Your bid was successfully placed"
bid_message_03 = "Your bid must be higher than: AU$ "
bid_message_04 = "Please enter a valid amount"
bid_message_05 = "Your bid must be higher than: AU$ "


@bid_blueprint.route('/')
@login_required
def bid():

    bids = Bid.query.filter_by(book_id=current_user.id).all()
    # Format watchlist.created_at date variable
    for item in bids:
        item.date_formatted = item.created_at.strftime('%d/%m/%Y')
    return "BID PAGE"


@bid_blueprint.route('/add/<book_id>/', methods=['POST', 'GET'])
@login_required
def bid_add(book_id):
    bid_amount = request.args.get('bid_amount')
    book = Book.query.filter_by(id=book_id).first()
    # If no bid amount was entered
    if bid_amount == "":
        return redirect(url_for('book.book_detail', book_id=book_id, message=bid_message_04))
    # If book is owned by the user show  watchlist_message_01
    if current_user.id == int(book.user_id):
        return redirect(url_for('book.book_detail', book_id=book_id, message=bid_message_01))
    else:
        bid = Bid(bid_amount, current_user.id, book_id)
        result = bid.add_bid()
        # If bid was valid
        if result == True:
            return redirect(url_for('book.book_detail', book_id=book_id, message=bid_message_02))
        # If bid was lass than the start bid amount
        elif result == False:
            start_amount = '{:.2f}'.format(book.start_bid_amount)
            return redirect(url_for('book.book_detail', book_id=book_id, message=bid_message_05+start_amount))
        # If bid was lass or equal to the highest bid amount.
        else:
            highest_amount = '{:.2f}'.format(result)
            return redirect(url_for('book.book_detail', book_id=book_id, message=bid_message_03+highest_amount))



