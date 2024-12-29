document.getElementById('switch-to-register').addEventListener('click', function(e) {
    e.preventDefault(); // Prevent default action
    document.getElementById('login-form').classList.remove('active');
    document.getElementById('register-form').classList.add('active');
});

document.getElementById('switch-to-login').addEventListener('click', function(e) {
    e.preventDefault(); // Prevent default action
    document.getElementById('register-form').classList.remove('active');
    document.getElementById('login-form').classList.add('active');
});

document.addEventListener("DOMContentLoaded", function() {
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.classList.add('fade-out');
            setTimeout(() => {
                flashMessages.remove(); // Remove from DOM after fade out
            }, 1000); // Match this duration with the CSS transition duration
        }, 1000); // Time before starting to fade out (3 seconds)
    }

    const flashMessagesRegister = document.getElementById('flash-messages-register');
    if (flashMessagesRegister) {
        setTimeout(() => {
            flashMessagesRegister.classList.add('fade-out');
            setTimeout(() => {
                flashMessagesRegister.remove(); // Remove from DOM after fade out
            }, 1000); // Match this duration with the CSS transition duration
        }, 1000); // Time before starting to fade out (3 seconds)
    }
});


//home page scripting

function searchMovie() {
    const query = document.getElementById('search-bar').value;
    // Implement search functionality using TMDB API
    // Redirect or update the page with search results
}

function addToWishlist(movieId) {
    fetch(`/add_to_wishlist/${movieId}`)
        .then(response => {
            if (response.ok) {
                alert('Movie added to wishlist!');
            } else {
                alert('Failed to add movie to wishlist.');
            }
        });
}

function showGenres() {
    // Implement genre search functionality
}

function toggleTheme() {
    const body = document.body;
    const themeToggleButton = document.getElementById('theme-toggle');

    // Toggle between light and dark mode
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        themeToggleButton.innerHTML = '🌙'; // Change to moon emoji
    } else {
        body.classList.add('dark-mode');
        themeToggleButton.innerHTML = '☀️'; // Change to sun emoji
    }
}
