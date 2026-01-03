/**
 * Authentication functionality
 */

// UI Elements
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const logoutBtn = document.getElementById('logout-btn');
const userMenu = document.getElementById('user-menu');
const loginModal = document.getElementById('login-modal');
const registerModal = document.getElementById('register-modal');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

// Show/Hide UI based on auth state
function updateAuthUI() {
    if (state.user) {
        loginBtn.style.display = 'none';
        registerBtn.style.display = 'none';
        userMenu.style.display = 'flex';
        document.getElementById('user-email').textContent = state.user.email;

        // Show role-specific navigation
        if (state.user.role === 'buyer') {
            document.getElementById('nav-orders').style.display = 'block';
            document.getElementById('cart-btn').style.display = 'block';
        } else if (state.user.role === 'seller') {
            document.getElementById('nav-seller').style.display = 'block';
        }
    } else {
        loginBtn.style.display = 'block';
        registerBtn.style.display = 'block';
        userMenu.style.display = 'none';
        document.getElementById('nav-orders').style.display = 'none';
        document.getElementById('nav-seller').style.display = 'none';
        document.getElementById('cart-btn').style.display = 'none';
    }
}

// Get current user info
async function getCurrentUser() {
    try {
        const user = await api.get('/api/auth/me');
        state.user = user;
        updateAuthUI();
        return user;
    } catch (error) {
        console.error('Failed to get user:', error);
        throw error;
    }
}

// Login
loginBtn.addEventListener('click', () => {
    openModal('login-modal');
});

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await api.post('/api/auth/login', { email, password });
        state.token = response.access_token;
        localStorage.setItem('token', response.access_token);

        await getCurrentUser();
        closeModal('login-modal');
        loginForm.reset();

        showNotification('Login successful!', 'success');
        loadProducts();
    } catch (error) {
        console.error('Login failed:', error);
    }
});

// Register
registerBtn.addEventListener('click', () => {
    openModal('register-modal');
});

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const role = document.getElementById('register-role').value;

    try {
        await api.post('/api/auth/register', { email, password, role });

        // Auto-login after registration
        const loginResponse = await api.post('/api/auth/login', { email, password });
        state.token = loginResponse.access_token;
        localStorage.setItem('token', loginResponse.access_token);

        await getCurrentUser();
        closeModal('register-modal');
        registerForm.reset();

        showNotification('Registration successful!', 'success');
        loadProducts();
    } catch (error) {
        console.error('Registration failed:', error);
    }
});

// Logout
logoutBtn.addEventListener('click', () => {
    state.user = null;
    state.token = null;
    state.cart = [];
    localStorage.removeItem('token');

    updateAuthUI();
    updateCartUI();
    showView('products');
    loadProducts();

    showNotification('Logged out successfully', 'info');
});
