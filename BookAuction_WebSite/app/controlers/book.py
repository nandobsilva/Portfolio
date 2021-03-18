from flask import Blueprint, render_template, request, session, redirect, abort, url_for, flash
from app.forms import AddBookForm, EditBookForm, UpdateBookForm
from werkzeug.utils import secure_filename
from app.models.book import Book
from app.models.bid import Bid
from app.models.review import Review
from app.functions import dateToString, appLocalPath, getHighestBid
from flask_login import login_required, current_user
from app.functions import getTop5, getBook
from app import db
import os

book_blueprint = Blueprint('book', __name__, url_prefix='/book')
log_in_message = "User must log in to access this page."


@book_blueprint.route('/my_books')
@login_required
def my_books():
    top5 = getTop5()
    booklist = Book.query.filter(Book.user_id.like(current_user.id)).all()
    for book in booklist:
        book.date_formatted = book.created_at.strftime('%d/%m/%Y')
        book.start_bid_amount_formatted = '{:.2f}'.format(book.start_bid_amount)
        book.highest_bid = getHighestBid(book.id)
    return render_template('book/my_books.html', books=booklist, top5=top5)


@book_blueprint.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        date = dateToString()
        target_folder = 'static/user_book_images'
        file = form.image.data
        BASE_PATH = appLocalPath()
        full_path = os.path.join(BASE_PATH, target_folder,
                                 secure_filename(str(current_user.id) + "-" + date + "_" + file.filename))
        file.save(full_path)
        relative_path = '/' + target_folder + '/' + secure_filename(
            str(current_user.id) + "-" + date + "_" + file.filename)
        # Create book object
        book = Book()
        book.title = form.title.data
        book.author = form.author.data
        book.category = form.category.data
        book.description = form.description.data
        book.isbn = form.isbn.data
        book.start_bid_amount = form.start_bid_amount.data
        book.user_id = current_user.id
        book.image_url = relative_path
        # Add book object in the database
        book.addBook()
        return redirect(url_for('book.my_books'))
    else:
        return render_template('book/add_book.html', form=form)


@book_blueprint.route('/edit/<book_id>', methods=["GET", "POST"])
@login_required
def edit(book_id):
    if request.method == "GET":
        print("GET")
        result = getBook(book_id)
        form = EditBookForm(result)
        return render_template('book/edit_book.html', form=form)

    if request.method == "POST":
        form = UpdateBookForm()
        print("POST")
        print(f"ISBN {form.isbn.data}")
        if form.validate_on_submit():
            print("Form valid")
            book = Book.query.filter_by(id=book_id).first()
            if book.user_id == current_user.id:
                print(f"Image data: {form.image.data}")
                # print(form.isbn.data)
                if form.image.data is not None:
                    date = dateToString()
                    target_folder = 'static/user_book_images'
                    file = form.image.data
                    BASE_PATH = appLocalPath()
                    full_path = os.path.join(BASE_PATH, target_folder,
                                             secure_filename(str(current_user.id) + "-" + date + "_" + file.filename))
                    file.save(full_path)
                    relative_path = '/' + target_folder + '/' + secure_filename(
                        str(current_user.id) + "-" + date + "_" + file.filename)
                # Create book object
                book.title = form.title.data
                book.author = form.author.data
                book.category = form.category.data
                book.description = form.description.data
                book.isbn = form.isbn.data
                book.start_bid_amount = float(book.start_bid_amount)
                if form.image.data is not None:
                    book.image_url = relative_path
                # Update book object in the database
                db.session.add(book)
                db.session.commit()
                print("Changes commited")
                return redirect(url_for('book.my_books'))
            else:
                print("User has no permission to change this book")
                return redirect(url_for('book.my_books'))
        else:
            print("Form not valid")
            return render_template('book/edit_book.html', form=form)


@book_blueprint.route('/update_status/<book_id>/<status>')
@login_required
def update_status(book_id, status):
    book = Book.query.filter_by(id=book_id).first()
    if book.user_id == current_user.id:
        Book.updateBookStatus(book_id, status)
        return redirect(url_for('book.my_books'))
    else:
        return redirect(url_for('user.logout'))


@book_blueprint.route('/book_detail')
@login_required
def book_detail():
    top5 = getTop5()
    message = request.args.get('message')
    book_id = request.args.get('book_id')
    book = Book.query.filter_by(id=book_id).first()
    page = 'book.book_detail'
    bids = Bid.query.filter_by(book_id=book_id).order_by(Bid.bid_amount).all()
    num_bids = 0
    reviews = Review.query.filter_by(book_id=book_id).order_by(Review.id).all()
    highest_bid = getHighestBid(book_id)
    show_bid_list = False
    if current_user.id == int(book.user_id):
        show_bid_list = True

    # Add a identifier, formatted_date and bid_amount_formatted in each bid row
    count = 1
    print(highest_bid)
    for bid in bids:
        num_bids += 1
        bid.num = num_bids
        bid.count = count
        bid.date_formatted = bid.created_at.strftime('%d/%m/%Y')
        bid.amount_formatted = '{:.2f}'.format(bid.bid_amount)
        count += 1
        bid.has_won = False
        if (float(highest_bid) == float(bid.bid_amount)) and (book.bid_status == "Closed"):
            bid.has_won = True
    for review in reviews:
        print(review.created_at)
        review.date_formatted = review.created_at.strftime('%d/%m/%Y - %H:%M:%S')

    # If user does not provide the book_id
    if book_id is None:
        return "Please select a book"
    # If there id no error messages
    if message is None:
        # Format created_at and bid_amount
        book.date_formatted = book.created_at.strftime('%d/%m/%Y')
        book.start_bid_amount_formatted = '{:.2f}'.format(book.start_bid_amount)
        return render_template('book/book_detail.html', book=book, book_id=book_id, bids=bids,
                               num_bids=num_bids, highest_bid=highest_bid, reviews=reviews, next=page,
                               top5=top5, show_bid_list=show_bid_list)
    # If there is error messages
    else:
        # Format created_at and bid_amount
        book.date_formatted = book.created_at.strftime('%d/%m/%Y')
        book.start_bid_amount_formatted = '{:.2f}'.format(book.start_bid_amount)
        return render_template('book/book_detail.html', book=book, book_id=book_id, bids=bids,
                               next=page, num_bids=num_bids, highest_bid=highest_bid, reviews=reviews,
                               message=message, top5=top5, show_bid_list=show_bid_list)



#@book_blueprint.route(404)
#def page_not_found(e):
    # note that we set the 404 status explicitly
#    return "<h1>ERROR 404 - PAGE NOT FOUND</h1>"
