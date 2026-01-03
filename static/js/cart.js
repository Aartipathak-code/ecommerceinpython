/**
 * Shopping cart functionality
 */

const cartBtn = document.getElementById('cart-btn');
const cartSidebar = document.getElementById('cart-sidebar');
const closeCartBtn = document.getElementById('close-cart');
const checkoutBtn = document.getElementById('checkout-btn');

// Toggle cart sidebar
cartBtn.addEventListener('click', () => {
    cartSidebar.classList.add('open');
});

closeCartBtn.addEventListener('click', () => {
    cartSidebar.classList.remove('open');
});

// Update cart UI
function updateCartUI() {
    const cartCount = document.getElementById('cart-count');
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');

    const totalItems = state.cart.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    cartCount.textContent = totalItems;
    cartTotal.textContent = `₹${Math.round(totalPrice).toLocaleString('en-IN')}`;

    if (state.cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🛒</div>
                <p>Your cart is empty</p>
            </div>
        `;
        checkoutBtn.disabled = true;
        return;
    }

    checkoutBtn.disabled = false;

    cartItems.innerHTML = state.cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-image">
                ${item.image_url ? `<img src="${item.image_url}" alt="${item.name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 0.5rem;">` : '🛍️'}
            </div>
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">₹${Math.round(item.price).toLocaleString('en-IN')} each</div>
                <div class="cart-item-controls">
                    <button onclick="updateCartQuantity(${item.product_id}, -1)">−</button>
                    <span class="cart-item-quantity">${item.quantity}</span>
                    <button onclick="updateCartQuantity(${item.product_id}, 1)">+</button>
                    <button onclick="removeFromCart(${item.product_id})" style="margin-left: auto; color: hsl(0, 70%, 60%);">✕</button>
                </div>
            </div>
        </div>
    `).join('');
}

// Update cart item quantity
function updateCartQuantity(productId, change) {
    const cartItem = state.cart.find(item => item.product_id === productId);
    if (!cartItem) return;

    const product = state.products.find(p => p.id === productId);
    const newQuantity = cartItem.quantity + change;

    if (newQuantity <= 0) {
        removeFromCart(productId);
        return;
    }

    if (product && newQuantity > product.stock) {
        showNotification('Cannot add more than available stock', 'error');
        return;
    }

    cartItem.quantity = newQuantity;
    updateCartUI();
}

// Remove item from cart
function removeFromCart(productId) {
    state.cart = state.cart.filter(item => item.product_id !== productId);
    updateCartUI();
    showNotification('Item removed from cart', 'info');
}

// Checkout
checkoutBtn.addEventListener('click', async () => {
    if (!state.user || state.user.role !== 'buyer') {
        showNotification('Please login as a buyer to checkout', 'error');
        return;
    }

    if (state.cart.length === 0) {
        showNotification('Your cart is empty', 'error');
        return;
    }

    try {
        const orderData = {
            items: state.cart.map(item => ({
                product_id: item.product_id,
                quantity: item.quantity
            }))
        };

        await api.post('/api/orders', orderData);

        showNotification('Order placed successfully!', 'success');
        state.cart = [];
        updateCartUI();
        cartSidebar.classList.remove('open');

        // Refresh products to update stock
        loadProducts();
    } catch (error) {
        console.error('Checkout failed:', error);
    }
});
