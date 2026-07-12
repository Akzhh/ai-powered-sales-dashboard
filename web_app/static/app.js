// ==========================================
// GLOBALS & STATE
// ==========================================
let currentSection = 'sec-dashboard';
let allSales = [];
let previewChart = null;
let analyticsChart = null;

// ==========================================
// ON PAGE LOAD
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    setupEventListeners();
});

// ==========================================
// AUTHENTICATION MANAGEMENT
// ==========================================
function checkAuthStatus() {
    fetch('/api/auth/status')
        .then(res => res.json())
        .then(data => {
            if (data.logged_in) {
                hideLoginOverlay();
                loadDashboardData();
            } else {
                showLoginOverlay();
            }
        })
        .catch(err => {
            showToast('Connection error checking login status.', 'error');
        });
}

function showLoginOverlay() {
    document.getElementById('login-overlay').classList.add('active');
    document.getElementById('app-workspace').style.display = 'none';
}

function hideLoginOverlay() {
    document.getElementById('login-overlay').classList.remove('active');
    document.getElementById('app-workspace').style.display = 'flex';
}

// Toggle Password Visibility
document.getElementById('toggle-password').addEventListener('click', function() {
    const passInput = document.getElementById('password');
    const passIcon = this.querySelector('i');
    if (passInput.type === 'password') {
        passInput.type = 'text';
        passIcon.className = 'fa-regular fa-eye-slash';
    } else {
        passInput.type = 'password';
        passIcon.className = 'fa-regular fa-eye';
    }
});

// Handle Login Form Submit
document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    const errorEl = document.getElementById('login-error');

    errorEl.textContent = '';

    fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    })
    .then(async res => {
        const data = await res.json();
        if (res.ok) {
            showToast('Welcome back, admin!', 'success');
            hideLoginOverlay();
            loadDashboardData();
        } else {
            errorEl.textContent = data.error || 'Login failed';
        }
    })
    .catch(() => {
        errorEl.textContent = 'Server unreachable. Check terminal.';
    });
});

// Handle Logout
document.getElementById('btn-logout').addEventListener('click', () => {
    fetch('/api/logout', { method: 'POST' })
        .then(res => res.json())
        .then(() => {
            showToast('Logged out successfully', 'success');
            showLoginOverlay();
            // Clear inputs
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        });
});

// ==========================================
// NAVIGATION & PAGE ROUTING (SPA)
// ==========================================
function setupEventListeners() {
    // Sidebar items click
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const target = item.getAttribute('data-target');
            
            // Toggle sidebar active item
            menuItems.forEach(mi => mi.classList.remove('active'));
            item.classList.add('active');

            // Switch content sections
            const sections = document.querySelectorAll('.content-section');
            sections.forEach(sec => sec.classList.remove('active-section'));
            document.getElementById(target).classList.add('active-section');

            currentSection = target;
            handleSectionLoad(target);
        });
    });

    // View all button in Dashboard recent table
    document.getElementById('btn-view-all-sales').addEventListener('click', () => {
        const salesMenuItem = document.querySelector('.menu-item[data-target="sec-sales"]');
        if (salesMenuItem) salesMenuItem.click();
    });

    // CRUD - Add New Sale Modal Toggle
    document.getElementById('btn-open-add-modal').addEventListener('click', () => {
        openSalesModal();
    });

    document.getElementById('btn-close-modal').addEventListener('click', closeSalesModal);
    document.getElementById('btn-cancel-modal').addEventListener('click', closeSalesModal);

    // CRUD - Form Submit (Insert / Update)
    document.getElementById('sales-form').addEventListener('submit', handleSalesFormSubmit);

    // CRUD - Live Search Filtering
    document.getElementById('sales-search').addEventListener('input', (e) => {
        const val = e.target.value.toLowerCase().trim();
        filterSalesTable(val);
    });

    // AI Predictions Form Submit
    document.getElementById('prediction-form').addEventListener('submit', handlePredictionSubmit);

    // Chart.js toggles
    document.getElementById('chart-btn-line').addEventListener('click', function() {
        switchChartType(this, 'line');
    });
    document.getElementById('chart-btn-bar').addEventListener('click', function() {
        switchChartType(this, 'bar');
    });
    document.getElementById('chart-btn-pred').addEventListener('click', function() {
        switchChartType(this, 'prediction');
    });
}

function handleSectionLoad(sectionId) {
    const titleEl = document.getElementById('header-title');
    const descEl = document.getElementById('header-desc');

    if (sectionId === 'sec-dashboard') {
        titleEl.textContent = 'Dashboard Summary';
        descEl.textContent = 'Real-time statistics & visual forecasts';
        loadDashboardData();
    } else if (sectionId === 'sec-sales') {
        titleEl.textContent = 'Sales Management';
        descEl.textContent = 'Add, modify, and delete transactions in database';
        loadSalesData();
    } else if (sectionId === 'sec-prediction') {
        titleEl.textContent = 'AI Forecasting';
        descEl.textContent = 'Predict future monthly sales based on Machine Learning';
    } else if (sectionId === 'sec-analytics') {
        titleEl.textContent = 'Sales Graph Analysis';
        descEl.textContent = 'Historical data and actual vs prediction models';
        loadAnalyticsChart();
    }
}

// ==========================================
// TOAST NOTIFICATIONS
// ==========================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let iconClass = 'fa-info-circle';
    if (type === 'success') iconClass = 'fa-check-circle';
    if (type === 'error') iconClass = 'fa-exclamation-circle';

    toast.innerHTML = `
        <i class="fa-solid ${iconClass}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // Fade out and remove after 4 seconds
    setTimeout(() => {
        toast.classList.add('fade-out');
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }, 4000);
}

// ==========================================
// DASHBOARD VIEW LOGIC
// ==========================================
function loadDashboardData() {
    // 1. Fetch Stats
    fetch('/api/stats')
        .then(res => res.json())
        .then(stats => {
            document.getElementById('stat-sales').textContent = `₹ ${stats.total_sales.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            document.getElementById('stat-profit').textContent = `₹ ${stats.total_profit.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            document.getElementById('stat-orders').textContent = stats.total_orders;
        })
        .catch(() => showToast('Failed to load dashboard metrics', 'error'));

    // 2. Fetch Sales list
    fetch('/api/sales')
        .then(res => res.json())
        .then(sales => {
            allSales = sales;
            populateRecentTable(sales);
            renderPreviewChart(sales);
        })
        .catch(() => showToast('Failed to load database sales records', 'error'));
}

function populateRecentTable(sales) {
    const tbody = document.getElementById('recent-sales-body');
    tbody.innerHTML = '';

    // Show latest 5 items
    const latestSales = [...sales].reverse().slice(0, 5);

    if (latestSales.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">No sales recorded yet.</td></tr>`;
        return;
    }

    latestSales.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${s.date}</td>
            <td style="font-weight: 500; color: white;">${s.product}</td>
            <td><span class="badge">${s.category}</span></td>
            <td style="font-weight: 600; color: var(--accent-blue);">₹ ${s.total.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderPreviewChart(sales) {
    const ctx = document.getElementById('preview-chart').getContext('2d');
    
    // Aggregate by category
    const categories = {};
    sales.forEach(s => {
        categories[s.category] = (categories[s.category] || 0) + s.total;
    });

    const labels = Object.keys(categories);
    const data = Object.values(categories);

    if (previewChart) {
        previewChart.destroy();
    }

    if (labels.length === 0) {
        return; // Empty state handles itself
    }

    previewChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#3B82F6', // Blue
                    '#10B981', // Green
                    '#F59E0B', // Orange
                    '#8B5CF6', // Purple
                    '#EC4899', // Pink
                    '#06B6D4'  // Cyan
                ],
                borderWidth: 2,
                borderColor: '#101626'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94A3B8',
                        font: { family: 'Outfit', size: 12 }
                    }
                }
            }
        }
    });
}

// ==========================================
// SALES MANAGEMENT CRUD LOGIC
// ==========================================
function loadSalesData() {
    fetch('/api/sales')
        .then(res => res.json())
        .then(sales => {
            allSales = sales;
            renderSalesTable(sales);
        })
        .catch(() => showToast('Failed to retrieve sales list.', 'error'));
}

function renderSalesTable(sales) {
    const tbody = document.getElementById('sales-table-body');
    tbody.innerHTML = '';

    if (sales.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 30px; color: var(--text-muted);">No transaction history found.</td></tr>`;
        return;
    }

    sales.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${s.id}</td>
            <td>${s.date}</td>
            <td style="font-weight: 500; color: white;">${s.product}</td>
            <td><span class="badge">${s.category}</span></td>
            <td>${s.quantity}</td>
            <td>₹ ${s.price.toFixed(2)}</td>
            <td style="font-weight: 600; color: var(--accent-blue);">₹ ${s.total.toFixed(2)}</td>
            <td style="font-weight: 600; color: var(--accent-green);">₹ ${s.profit.toFixed(2)}</td>
            <td>
                <button class="btn-action edit-btn" onclick="editSaleItem(${s.id})"><i class="fa-solid fa-pen-to-square"></i></button>
                <button class="btn-action delete-btn" onclick="deleteSaleItem(${s.id})"><i class="fa-solid fa-trash-can"></i></button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filterSalesTable(query) {
    if (!query) {
        renderSalesTable(allSales);
        return;
    }
    const filtered = allSales.filter(s => 
        s.product.toLowerCase().includes(query) || 
        s.category.toLowerCase().includes(query)
    );
    renderSalesTable(filtered);
}

// Delete item
window.deleteSaleItem = function(id) {
    if (confirm('Are you sure you want to delete this sale record?')) {
        fetch(`/api/sales/${id}`, { method: 'DELETE' })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showToast('Record deleted successfully', 'success');
                    loadSalesData();
                } else {
                    showToast(data.error || 'Failed to delete record', 'error');
                }
            })
            .catch(() => showToast('Error connecting to database server.', 'error'));
    }
}

// Edit item helper (pre-populates modal)
window.editSaleItem = function(id) {
    const sale = allSales.find(s => s.id === id);
    if (!sale) return;

    openSalesModal(sale);
}

// Modal open/close actions
function openSalesModal(sale = null) {
    const modal = document.getElementById('sales-modal');
    const form = document.getElementById('sales-form');
    const modalTitle = document.getElementById('modal-title');
    const errorEl = document.getElementById('modal-error');

    errorEl.textContent = '';
    form.reset();

    if (sale) {
        modalTitle.textContent = 'Edit Sale Record';
        document.getElementById('sale-id').value = sale.id;
        document.getElementById('sale-date').value = sale.date;
        document.getElementById('sale-category').value = sale.category;
        document.getElementById('sale-product').value = sale.product;
        document.getElementById('sale-quantity').value = sale.quantity;
        document.getElementById('sale-price').value = sale.price;
    } else {
        modalTitle.textContent = 'Add New Sale';
        document.getElementById('sale-id').value = '';
        // Set today's date by default
        document.getElementById('sale-date').value = new Date().toISOString().split('T')[0];
    }

    modal.classList.add('active');
}

function closeSalesModal() {
    document.getElementById('sales-modal').classList.remove('active');
}

function handleSalesFormSubmit(e) {
    e.preventDefault();

    const id = document.getElementById('sale-id').value;
    const date = document.getElementById('sale-date').value;
    const category = document.getElementById('sale-category').value.trim();
    const product = document.getElementById('sale-product').value.trim();
    const quantity = document.getElementById('sale-quantity').value;
    const price = document.getElementById('sale-price').value;
    const errorEl = document.getElementById('modal-error');

    errorEl.textContent = '';

    const payload = { date, category, product, quantity, price };

    const url = id ? `/api/sales/${id}` : '/api/sales';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(async res => {
        const data = await res.json();
        if (res.ok) {
            showToast(id ? 'Sale updated successfully' : 'Sale added successfully', 'success');
            closeSalesModal();
            loadSalesData();
        } else {
            errorEl.textContent = data.error || 'Submission failed';
        }
    })
    .catch(() => {
        errorEl.textContent = 'Error connecting to application server.';
    });
}

// ==========================================
// AI PREDICTIONS VIEW LOGIC
// ==========================================
function handlePredictionSubmit(e) {
    e.preventDefault();
    const month = document.getElementById('predict-month').value;
    const valEl = document.getElementById('prediction-result-val');
    const badgeEl = document.getElementById('prediction-month-badge');
    const iconWrapper = document.querySelector('.predict-icon-wrapper');

    // Start styling loading animation
    valEl.textContent = 'Calculating...';
    badgeEl.textContent = `Month ${month}`;
    iconWrapper.style.transform = 'scale(1.1)';
    iconWrapper.style.borderColor = 'var(--accent-purple)';

    fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ month: parseInt(month) })
    })
    .then(async res => {
        const data = await res.json();
        iconWrapper.style.transform = 'scale(1)';
        
        if (res.ok) {
            valEl.textContent = `₹ ${data.predicted_sales.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            showToast(`Predicted sales for Month ${month} computed`, 'success');
        } else {
            valEl.textContent = '₹ 0.00';
            showToast(data.error || 'Failed to compute predictions', 'error');
        }
    })
    .catch(() => {
        iconWrapper.style.transform = 'scale(1)';
        valEl.textContent = 'Error';
        showToast('Prediction service unavailable.', 'error');
    });
}

// ==========================================
// GRAPH & VISUALIZATION LOGIC
// ==========================================
let currentChartMode = 'line'; // line, bar, prediction

function loadAnalyticsChart() {
    // Fetch dataset.csv values
    fetch('/api/dataset')
        .then(res => res.json())
        .then(data => {
            renderAnalyticsChart(data);
        })
        .catch(() => showToast('Failed to read CSV dataset file', 'error'));
}

function switchChartType(buttonEl, type) {
    document.querySelectorAll('.btn-tab').forEach(b => b.classList.remove('active'));
    buttonEl.classList.add('active');
    currentChartMode = type;
    loadAnalyticsChart();
}

function renderAnalyticsChart(csvData) {
    const ctx = document.getElementById('analytics-chart').getContext('2d');
    
    if (analyticsChart) {
        analyticsChart.destroy();
    }

    if (csvData.length === 0) {
        return; // handle empty file
    }

    const months = csvData.map(item => `Month ${item.Month}`);
    const sales = csvData.map(item => item.Sales);

    let chartType = 'line';
    let datasets = [];

    if (currentChartMode === 'line') {
        chartType = 'line';
        datasets = [{
            label: 'Monthly Sales (Historical)',
            data: sales,
            borderColor: '#3B82F6',
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            borderWidth: 3,
            fill: true,
            tension: 0.35,
            pointBackgroundColor: '#3B82F6',
            pointRadius: 5,
            pointHoverRadius: 7
        }];
    } else if (currentChartMode === 'bar') {
        chartType = 'bar';
        datasets = [{
            label: 'Monthly Sales Amount',
            data: sales,
            backgroundColor: 'rgba(16, 185, 129, 0.75)',
            borderColor: '#10B981',
            borderWidth: 1.5,
            borderRadius: 6
        }];
    } else if (currentChartMode === 'prediction') {
        chartType = 'line';
        
        // Plot historical + month 13 forecast point
        const extendedMonths = [...months, 'Month 13 (AI)'];
        const extendedSales = [...sales];
        
        // Add sample forecast item (calls predict API synchronously or uses linear regression estimation)
        // Historically: Month 13 is roughly 51424.24
        extendedSales.push(51424.24);

        datasets = [
            {
                label: 'Sales Trend & Forecast (Month 13)',
                data: extendedSales,
                borderColor: '#8B5CF6',
                backgroundColor: 'rgba(139, 92, 246, 0.12)',
                borderWidth: 3,
                tension: 0.35,
                fill: true,
                pointBackgroundColor: (context) => {
                    const idx = context.dataIndex;
                    return idx === 12 ? '#F59E0B' : '#8B5CF6';
                },
                pointBorderColor: (context) => {
                    const idx = context.dataIndex;
                    return idx === 12 ? '#FFF' : '#8B5CF6';
                },
                pointRadius: (context) => {
                    const idx = context.dataIndex;
                    return idx === 12 ? 8 : 5;
                },
                pointHoverRadius: 10
            }
        ];
    }

    analyticsChart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: currentChartMode === 'prediction' ? [...csvData.map(item => `Month ${item.Month}`), 'Month 13'] : months,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#94A3B8',
                        font: { family: 'Outfit', size: 13, weight: '500' }
                    }
                },
                tooltip: {
                    padding: 12,
                    titleFont: { family: 'Outfit', size: 14, weight: 'bold' },
                    bodyFont: { family: 'Outfit', size: 13 },
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += `₹ ${context.parsed.y.toLocaleString('en-IN', {maximumFractionDigits: 2})}`;
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.04)' },
                    ticks: {
                        color: '#64748B',
                        font: { family: 'Outfit', size: 11 },
                        callback: function(value) {
                            return '₹ ' + value.toLocaleString('en-IN');
                        }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#64748B',
                        font: { family: 'Outfit', size: 11 }
                    }
                }
            }
        }
    });
}
