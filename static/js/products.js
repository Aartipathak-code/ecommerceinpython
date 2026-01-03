/**
 * Product browsing and management functionality
 */

// Load all products
async function loadProducts(search = '') {
    try {
        const endpoint = search ? `/api/products?search=${encodeURIComponent(search)}` : '/api/products';
        const products = await api.get(endpoint);
        state.products = products;
        displayProducts(products);
    } catch (error) {
        console.error('Failed to load products:', error);
    }
}

// Display products in grid
function displayProducts(products) {
    const grid = document.getElementById('products-grid');

    if (products.length === 0) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <div class="empty-state-icon">📦</div>
                <h3>No products found</h3>
                <p>Check back later for new products!</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = products.map(product => `
        <div class="product-card" data-id="${product.id}">
            <div class="product-image">
                ${product.image_url ? `<img src="${product.image_url}" alt="${product.name}">` : '🛍️'}
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description || 'No description available'}</p>
                <div class="product-footer">
                    <span class="product-price">₹${Math.round(product.price).toLocaleString('en-IN')}</span>
                    <span class="product-stock">${product.stock} in stock</span>
                </div>
                ${state.user?.role === 'buyer' ? `
                    <div class="product-actions">
                        <button class="btn-primary" onclick="addToCart(${product.id})" ${product.stock === 0 ? 'disabled' : ''}>
                            ${product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
                        </button>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Add product to cart
function addToCart(productId) {
    if (!state.user || state.user.role !== 'buyer') {
        showNotification('Please login as a buyer to add items to cart', 'error');
        return;
    }

    const product = state.products.find(p => p.id === productId);
    if (!product) return;

    const cartItem = state.cart.find(item => item.product_id === productId);

    if (cartItem) {
        if (cartItem.quantity < product.stock) {
            cartItem.quantity++;
        } else {
            showNotification('Cannot add more than available stock', 'error');
            return;
        }
    } else {
        state.cart.push({
            product_id: productId,
            name: product.name,
            price: product.price,
            quantity: 1,
            image_url: product.image_url
        });
    }

    updateCartUI();
    showNotification(`${product.name} added to cart`, 'success');
}

// Seller: Load seller's products
async function loadSellerProducts() {
    if (!state.user || state.user.role !== 'seller') return;

    try {
        const products = await api.get('/api/products/seller/my-products');
        displaySellerProducts(products);
    } catch (error) {
        console.error('Failed to load seller products:', error);
    }
}

// Display seller's products
function displaySellerProducts(products) {
    const grid = document.getElementById('seller-products-grid');

    if (products.length === 0) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <div class="empty-state-icon">📦</div>
                <h3>No products yet</h3>
                <p>Click "Add Product" to list your first product!</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image">
                ${product.image_url ? `<img src="${product.image_url}" alt="${product.name}">` : '🛍️'}
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description || 'No description'}</p>
                <div class="product-footer">
                    <span class="product-price">₹${Math.round(product.price).toLocaleString('en-IN')}</span>
                    <span class="product-stock">${product.stock} in stock</span>
                </div>
                <div class="product-actions">
                    <button class="btn-secondary" onclick="editProduct(${product.id})">Edit</button>
                    <button class="btn-secondary" onclick="deleteProduct(${product.id})">Delete</button>
                </div>
            </div>
        </div>
    `).join('');
}

// Helper function to convert file to Base64
function convertToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

// Helper function to show image preview
function showImagePreview(imageData) {
    const preview = document.getElementById('image-preview');
    if (imageData) {
        preview.innerHTML = `
            <div style="text-align: center;">
                <img src="${imageData}" 
                     alt="Preview" 
                     style="max-width: 100%; max-height: 200px; border-radius: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <p style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-muted);">Image preview</p>
            </div>
        `;
    } else {
        preview.innerHTML = '';
    }
}

// Handle file upload
document.getElementById('product-image-file').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            showNotification('Image too large. Please use an image under 5MB', 'error');
            e.target.value = ''; // Clear the file input
            return;
        }

        // Validate file type
        if (!file.type.startsWith('image/')) {
            showNotification('Please select an image file', 'error');
            e.target.value = '';
            return;
        }

        try {
            const base64 = await convertToBase64(file);
            document.getElementById('product-image-url').value = base64;
            showImagePreview(base64);
            showNotification('Image loaded successfully', 'success');
        } catch (error) {
            showNotification('Failed to load image', 'error');
            console.error('Image conversion error:', error);
        }
    }
});

// Handle URL input - show preview when URL is entered
document.getElementById('product-image-url').addEventListener('input', (e) => {
    const url = e.target.value;
    if (url && (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:'))) {
        showImagePreview(url);
    } else if (!url) {
        showImagePreview(null);
    }
});

// Add Product Button
document.getElementById('add-product-btn').addEventListener('click', () => {
    state.editingProduct = null;
    document.getElementById('product-modal-title').textContent = 'Add Product';
    document.getElementById('product-form').reset();
    document.getElementById('product-image-file').value = ''; // Clear file input
    showImagePreview(null); // Clear preview
    openModal('product-modal');
});

// Product Form Submit
document.getElementById('product-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const productData = {
        name: document.getElementById('product-name').value,
        description: document.getElementById('product-description').value,
        price: parseFloat(document.getElementById('product-price').value),
        stock: parseInt(document.getElementById('product-stock').value),
        image_url: document.getElementById('product-image-url').value || null
    };

    try {
        if (state.editingProduct) {
            await api.put(`/api/products/${state.editingProduct}`, productData);
            showNotification('Product updated successfully', 'success');
        } else {
            await api.post('/api/products', productData);
            showNotification('Product created successfully', 'success');
        }

        closeModal('product-modal');
        loadSellerProducts();
        loadProducts(); // Refresh main products view
    } catch (error) {
        console.error('Failed to save product:', error);
    }
});

// Edit product
async function editProduct(productId) {
    try {
        const product = await api.get(`/api/products/${productId}`);

        state.editingProduct = productId;
        document.getElementById('product-modal-title').textContent = 'Edit Product';
        document.getElementById('product-name').value = product.name;
        document.getElementById('product-description').value = product.description || '';
        document.getElementById('product-price').value = product.price;
        document.getElementById('product-stock').value = product.stock;
        document.getElementById('product-image-url').value = product.image_url || '';
        document.getElementById('product-image-file').value = ''; // Clear file input

        // Show preview if image exists
        if (product.image_url) {
            showImagePreview(product.image_url);
        } else {
            showImagePreview(null);
        }

        openModal('product-modal');
    } catch (error) {
        console.error('Failed to load product:', error);
    }
}

// Delete product
async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) return;

    try {
        await api.delete(`/api/products/${productId}`);
        showNotification('Product deleted successfully', 'success');
        loadSellerProducts();
        loadProducts();
    } catch (error) {
        console.error('Failed to delete product:', error);
    }
}
