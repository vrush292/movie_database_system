from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, User  # Assuming you have a User model defined
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return render_template('index.html')  # Your login page

@api.route('/home')
def home():
    return render_template('home.html')  # Your home page

@api.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        flash('Login successful!', 'success')
        return redirect(url_for('api.home'))  # Redirect to home.html on successful login
    else:
        flash('Login failed. Check your username and password.', 'danger')
        return redirect(url_for('api.index'))  # Redirect back to index.html on failure

@api.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # Check if the user already exists
    if User.query.filter_by(username=username).first():
        flash('Username already exists. Please choose a different one.', 'danger')
        return redirect(url_for('api.index'))  # Redirect back to index.html

    # Create a new user
    new_user = User(username=username, email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    
    flash('Registration successful! You can now log in.', 'success')
    return redirect(url_for('api.index'))  # Redirect back to index.html