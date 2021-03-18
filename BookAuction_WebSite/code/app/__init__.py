from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

def create_app() -> Flask:
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    # Database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)
    db.init_app(app)

    # Define where app_images uploaded by the user will be stored
    app.config['UPLOAD_FOLDER'] = 'static/user_book_images'

    # Secret key used by the app
    app.secret_key = '%test_01_Secret_key?'

    # Resolve circular dependency
    from app.controlers.user import user_blueprint
    from app.controlers.home import home_blueprint
    from app.controlers.book import book_blueprint
    from app.controlers.bid import bid_blueprint
    from app.controlers.review import review_blueprint
    from app.controlers.watchlist import watchlist_blueprint
    from app.controlers.error_handler import errors

    # Create database tables
    from app.models.user import User
    from app.models.book import Book
    from app.models.watchlist import Watchlist
    from app.models.bid import Bid
    from app.models.review import Review

    # Register blueprints used in the app
    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(book_blueprint)
    app.register_blueprint(watchlist_blueprint)
    app.register_blueprint(review_blueprint)
    app.register_blueprint(bid_blueprint)
    app.register_blueprint(errors)

    return app

