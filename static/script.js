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

