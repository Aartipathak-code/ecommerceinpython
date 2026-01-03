/**
 * Order management functionality
 */

// Load buyer orders
async function loadOrders() {
    if (!state.user || state.user.role !== 'buyer') return;

    try {
        const orders = await api.get('/api/orders');
        state.orders = orders;
        displayOrders(orders);
    } catch (error) {
        console.error('Failed to load orders:', error);
    }
}

// Display buyer orders
function displayOrders(orders) {
    const ordersList = document.getElementById('orders-list');

    if (orders.length === 0) {
        ordersList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <h3>No orders yet</h3>
                <p>Start shopping to place your first order!</p>
            </div>
        `;
        return;
    }

    ordersList.innerHTML = orders.map(order => `
        <div class="order-card">
            <div class="order-header">
                <span class="order-id">Order #${order.id}</span>
                <span class="order-status ${order.status}">${order.status.toUpperCase()}</span>
            </div>
            <div class="order-items">
                ${order.items.map(item => `
                    <div class="order-item">
                        <span>Product ID: ${item.product_id} × ${item.quantity}</span>
                        <span>₹${Math.round(item.price * item.quantity).toLocaleString('en-IN')}</span>
                    </div>
                `).join('')}
            </div>
            <div class="order-total">
                <span>Total:</span>
                <span>₹${Math.round(order.total_amount).toLocaleString('en-IN')}</span>
            </div>
            <div style="margin-top: 0.5rem; color: var(--text-muted); font-size: 0.875rem;">
                ${new Date(order.created_at).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })}
            </div>
        </div>
    `).join('');
}

// Load seller orders
async function loadSellerOrders() {
    if (!state.user || state.user.role !== 'seller') return;

    try {
        const orders = await api.get('/api/orders/seller/orders');
        displaySellerOrders(orders);
    } catch (error) {
        console.error('Failed to load seller orders:', error);
    }
}

// Display seller orders
function displaySellerOrders(orders) {
    const ordersList = document.getElementById('seller-orders-list');

    if (orders.length === 0) {
        ordersList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <h3>No orders yet</h3>
                <p>Orders for your products will appear here!</p>
            </div>
        `;
        return;
    }

    // Group by order ID
    const groupedOrders = orders.reduce((acc, item) => {
        if (!acc[item.order_id]) {
            acc[item.order_id] = {
                order_id: item.order_id,
                buyer_email: item.buyer_email,
                order_status: item.order_status,
                items: []
            };
        }
        acc[item.order_id].items.push(item);
        return acc;
    }, {});

    ordersList.innerHTML = Object.values(groupedOrders).map(order => {
        const total = order.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        return `
            <div class="order-card">
                <div class="order-header">
                    <span class="order-id">Order #${order.order_id}</span>
                    <span class="order-status ${order.order_status}">${order.order_status.toUpperCase()}</span>
                </div>
                <div style="margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.875rem;">
                    Buyer: ${order.buyer_email}
                </div>
                <div class="order-items">
                    ${order.items.map(item => `
                        <div class="order-item">
                            <span>${item.product_name} × ${item.quantity}</span>
                            <span>₹${Math.round(item.price * item.quantity).toLocaleString('en-IN')}</span>
                        </div>
                    `).join('')}
                </div>
                <div class="order-total">
                    <span>Total:</span>
                    <span>₹${Math.round(total).toLocaleString('en-IN')}</span>
                </div>
            </div>
        `;
    }).join('');
}
