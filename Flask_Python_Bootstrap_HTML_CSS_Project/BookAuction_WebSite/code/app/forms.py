from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, FileField, SelectField, DecimalField, \
    IntegerField, Label
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Regexp
from flask_wtf.file import FileRequired, FileField, FileAllowed
from app.models.book import Book
from app.functions import appLocalPath
from flask import session
from flask_bootstrap import Bootstrap


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        InputRequired("Email is required"), Email('Invalid email address')])

    password = PasswordField('Password', validators=[
        InputRequired('Password is required.')])

    # submit = SubmitField('Log in')


class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired("Name is required"),
                                           Length(min=2, max=30,
                                                  message=f"Name must have minimum 2 and \nmaximum 30 characters")])

    email = StringField("Email", validators=[InputRequired("Email is required"), Email('Enter a valid email')])

    password = PasswordField('Password', validators=[InputRequired('Password is required.'),
                                                     Length(min=6, message="Password must have minimum 6 characters")])

    confirm_password = PasswordField("Confirm password", validators=[InputRequired("Confirm password is required"),
                                                                     EqualTo('password',
                                                                             message='Password does not match')])

    phone = StringField('Phone number', validators=[InputRequired('Phone number is required'),
                                                    Length(min=8, max=10,
                                                           message="Please enter a valida phone number \n(Example: 0298765432)"),
                                                    Regexp("^[0-9]*$",
                                                           message="Please enter a valida phone number \n(Example: 0298765432)")])
    address = TextAreaField('Address', validators=[
        Length(min=10, max=60, message="Address must have minimum 10 and \nmaximum 60 characters"),
        InputRequired('Address is required')])

    submit = SubmitField("Sign up")


class AddBookForm(FlaskForm):
    allowed_files = {'png', 'PNG', 'jpg', 'JPG'}

    image = FileField('', validators=[FileRequired('Image is required'),
                                      FileAllowed(allowed_files, message='The website supports just .png and .jpg files')])

    title = TextAreaField('Title', validators=[InputRequired('Title is required'),
                                               Length(min=2, max=100, message="Title must have minimum 2 and maximum 50 characters")])

    author = TextAreaField('Author', validators=[Length(max=40, message="Author must have maximum 40 characters"),
                                     InputRequired('Author is required')])

    category = SelectField('Category', choices=["", 'Academic', 'Action', 'Adventure', 'Biographies', 'Business',
                                                'Cooking', 'Comic', 'Detective', 'Drama', 'Fantasy', 'Fiction',
                                                'History', 'Kids', 'Poetry', 'Romance', 'Sci-Fi', 'Self-Help',
                                                'Thriller', 'Others'],
                                       validators=[InputRequired('Category is required')])

    description = TextAreaField('Description',
                                validators=[Length(max=400, message="Description must have maximum 400 characters")])

    isbn = TextAreaField('ISBN', validators=[Length(max=30, message="ISBN must have maximum 30 characters")])

    start_bid_amount = DecimalField('Star bid amount', places=2,
                                    validators=[NumberRange(min=0, max=100.000,message="Amount must be between 0.00 and 100,000.00"),
                                    InputRequired('Amount is required')])

    submit = SubmitField("Add book")


class EditBookForm(FlaskForm, ):
    def __init__(self, book, *args, **kwargs):
        super(EditBookForm, self).__init__(*args, **kwargs)
        BASE_PATH = appLocalPath()
        self.title.data = book.title
        self.author.data = book.author
        self.category.data = book.category
        self.description.data = book.description
        self.isbn.data = book.isbn
        # self.image.data = open(BASE_PATH+book.image_url,"r")

    allowed_files = {'png', 'PNG', 'jpg', 'JPG'}

    image = FileField('Image', validators=[FileAllowed(allowed_files,
                                                       message='The website supports just .png and .jpg files')])

    title = TextAreaField('Title', validators=[InputRequired('Title is required'), Length(min=2, max=100,
                                                                                          message="Title must have minimum 2 and maximum 50 characters")])

    author = TextAreaField('Author', validators=[Length(max=40, message="Author must have maximum 40 characters"),
                                                 InputRequired('Author is required')])

    category = SelectField('Category',
                           choices=["", 'Academic', 'Action', 'Adventure', 'Biographies', 'Business',
                                    'Cooking', 'Comic', 'Detective', 'Drama', 'Fantasy', 'Fiction',
                                    'History', 'Kids', 'Poetry', 'Romance', 'Sci-Fi', 'Self-Help',
                                    'Thriller', 'Others'], validators=[InputRequired('Category is required')])

    description = TextAreaField('Description', validators=[
        Length(max=400, message="Description must have maximum 200 characters")])

    isbn = TextAreaField('ISBN', validators=[Length(max=30, message="ISBN must have maximum 30 characters")])

    submit = SubmitField("Save changes")


class UpdateBookForm(FlaskForm):
    allowed_files = {'png', 'PNG', 'jpg', 'JPG'}
    image = FileField('',
                      validators=[FileAllowed(allowed_files, message='The website supports just .png and .jpg files')])
    title = TextAreaField('Title', validators=[InputRequired('Title is required'),
                                               Length(min=2, max=100, message="Title must have minimum 2 and maximum 50 characters")])
    author = TextAreaField('Author', validators=[Length(max=40, message="Author must have maximum 40 characters"),
                                                 InputRequired('Author is required')])
    category = SelectField('Category',
                           choices=["", 'Academic', 'Action', 'Adventure', 'Biographies', 'Business',
                                    'Cooking', 'Comic', 'Detective', 'Drama', 'Fantasy', 'Fiction',
                                    'History', 'Kids', 'Poetry', 'Romance', 'Sci-Fi', 'Self-Help',
                                    'Thriller', 'Others'], validators=[InputRequired('Category is required')])

    description = TextAreaField('Description',
                                validators=[Length(max=400, message="Description must have maximum 200 characters")])

    isbn = TextAreaField('ISBN', validators=[Length(max=30, message="ISBN must have maximum 30 characters")])


class AddBidForm(FlaskForm):
    bid_amount = DecimalField('Star bid amount', places=2, validators=[InputRequired('Amount is required')])
