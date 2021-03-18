from flask import Blueprint, render_template, request, session, redirect, abort, url_for
from flask_login import login_required, current_user
from app.models.review import Review
from app.models.book import Book


review_blueprint = Blueprint('review', __name__, url_prefix='/review')

bid_message_01 = "You can not add a review in this book because you are the owner of it"
bid_message_02 = "Your review was successfully posted"
bid_message_03 = "Please enter a valid review"


@review_blueprint.route('/')
@login_required
def review():
    return "REVIEW PAGE"


@review_blueprint.route('/add/<book_id>', methods=['POST', 'GET'])
@login_required
def add_review(book_id):
    review = request.args.get('review')
    print(f"Review: {review}")
    book = Book.query.filter_by(id=book_id).first()
    if review == "":
        return redirect(url_for('book.book_detail', book_id=book_id, message=bid_message_03))
    # If book is owned by the current user show  watchlist_message_01
    if current_user.id == int(book.user_id):
        return redirect(url_for('book.book_detail', book_id=book_id, message=bid_message_01))
    # If book is not owned by the current user.
    else:
        review = Review(current_user.id, book_id, review)
        result = review.add_review()
        return redirect(url_for('book.book_detail', book_id=book_id, message=bid_message_02))
