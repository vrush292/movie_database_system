from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, User, Movie, Wishlist  # Assuming you have a User model defined
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask_login import login_user, logout_user, login_required, current_user

# API routes
api = Blueprint('api', __name__)

@api.route('/')
def index():
    return render_template('index.html')  # Your login page

@api.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)  # Create a user session
        flash('Login successful!', 'success')
        return redirect(url_for('main_routes.home'))  # Redirect to home.html on successful login
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

@api.route('/signout')
def signout():
    logout_user()  # This will remove the user session
    flash('You have been signed out.', 'info')
    return redirect(url_for('api.index'))  # Redirect to the login page

# Home page logic implementation
main_routes = Blueprint('main_routes', __name__)

TMDB_API_KEY = '75439a8f9e551d13a91c261aa1062e5e'  # Replace with your TMDB API key

@main_routes.route('/home')
@login_required  # Protect this route
def home():
    trending_movies = get_trending_movies()
    return render_template('home.html', trending_movies=trending_movies, movies=None)

def get_trending_movies():
    try:
        response = requests.get(f'https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}')
        response.raise_for_status()  # Raise an error for bad responses
        return response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending movies: {e}")
        flash('Error fetching trending movies. Please try again later.', 'danger')
        return []

@main_routes.route('/movie/<int:movie_id>')
@login_required  # Protect this route
def movie_details(movie_id):
    movie = get_movie_details(movie_id)
    return render_template('movie_details.html', movie=movie)

def get_movie_details(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits,videos,reviews')
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details: {e}")
        flash('Error fetching movie details. Please try again later.', 'danger')
        return {}

@main_routes.route('/search', methods=['GET'])
@login_required  # Protect this route
def search_movies():
    query = request.args.get('query')
    movies = []  # Initialize movies as an empty list

    if query:
        try:
            response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}')
            response.raise_for_status()  # Raise an error for bad responses
            movies = response.json().get('results', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching search results: {e}")
    flash('Error fetching search results. Please try again later.', 'danger')

    return render_template('home.html', movies=movies, trending_movies=get_trending_movies())  # Pass the movies list to the template

@main_routes.route('/toggle_wishlist/<int:movie_id>', methods=['POST'])
@login_required  # Protect this route
def toggle_wishlist(movie_id):
    # Check if the movie is already in the user's wishlist
    wishlist_item = Wishlist.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
    
    if wishlist_item:
        # If it exists, remove it from the wishlist
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Movie removed from your wishlist!', 'success')
    else:
        # If it does not exist, add it to the wishlist
        wishlist_item = Wishlist(movie_id=movie_id, user_id=current_user.id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash('Movie added to your wishlist!', 'success')
    
    return redirect(url_for('main_routes.movie_details', movie_id=movie_id))  # Redirect back to the movie details page

@main_routes.route('/wishlist')
@login_required  # Protect this route
def wishlist():
    user_wishlist = Wishlist.query.filter_by(user_id=current_user.id).all()  # Fetch user's wishlist
    movies = [Movie.query.get(item.movie_id) for item in user_wishlist]  # Get movie details for each wishlist item
    return render_template('wishlist.html', movies=movies)  # Pass the movies list to the template

@main_routes.route('/recommendation')
@login_required  # Protect this route
def recommendation():
    return render_template('recommendation.html')

@main_routes.route('/profile')
@login_required  # Protect this route
def profile():
    return render_template('profile.html')

@main_routes.route('/about')
@login_required  # Protect this route
def about():
    return render_template('about.html')

