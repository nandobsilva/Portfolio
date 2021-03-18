from flask import Blueprint, render_template, request, session, redirect, abort, url_for
from app.models.book import Book
from app.models.bid import Bid
from app import db
from app.functions import getTop5, getHighestBid
from flask_login import login_required, current_user
from flask_login import UserMixin
from app.models.user import User
from sqlalchemy import func

import re

home_blueprint = Blueprint('home', __name__, url_prefix='/')
log_in_message = "User must log in to access this page."

@home_blueprint.route('/')
def index():
    session.clear()
    return redirect(url_for('home.home'))


@home_blueprint.route('/home', methods=['GET', 'POST'])

def home():
    message = request.args.get('message')
    page = 'home.home'
    booklist = Book.query.filter().all()
    categories = []
    booklist_filtered = []
    for book in booklist:
        book.bids = 0
        book.highest_bid = getHighestBid(book.id)
        if book.category not in categories:
            categories.append(book.category)
        booklist_filtered.append(book)
    categories.sort()


    # TOP5 Books: Books with higher number of bids
    top5 = getTop5()

    # Render page
    if request.method == 'GET':
        # If there is no Message to show to the user
        if message is None:
            return render_template('home/home.html', search=True, books=booklist, categories=categories,
                                   message="", page=page, top5=top5)
        else:
            return render_template('home/home.html', search=True, books=booklist, categories=categories,
                                   message=message, page=page, top5=top5)
    else:
        # Search bar variables
        title = request.values.get('title')
        author = request.values.get('author')
        isbn = request.values.get('isbn')
        category = request.values.get('category')

        # Filter by category
        if category != "Category (All)":
            new_list = []
            for book in booklist_filtered:
                if book.category == category:
                   new_list.append(book)
            booklist_filtered = new_list
        # Filter by title
        if title != "":
            new_list = []
            for book in booklist_filtered:
                filter = re.findall(title.lower(), book.title.lower())
                if filter != []:
                    new_list.append(book)
            booklist_filtered = new_list
        # filter by author
        if author != "":
            new_list = []
            for book in booklist_filtered:
                filter = re.findall(author.lower(), book.author.lower())
                if filter != []:
                    new_list.append(book)
            booklist_filtered = new_list
        # filter by isbn
        if isbn != "":
            new_list = []
            for book in booklist_filtered:
                filter = re.findall(isbn.lower(), book.isbn.lower())
                if filter != []:
                    new_list.append(book)
            booklist_filtered = new_list

        if message is None:
            return render_template('home/home.html', search=True, books=booklist_filtered, categories=categories, message="",
                                   page=page, title=title, author=author, isbn=isbn, category=category, top5=top5)
        else:
            return render_template('home/home.html', search=True, books=booklist_filtered, categories=categories,
                                   message=message, page=page, title=title, author=author, isbn=isbn, category=category, top5=top5)


