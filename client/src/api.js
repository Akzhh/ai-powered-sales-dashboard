// ==========================================
// Centralized API Client
// ==========================================

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

async function request(url, options = {}) {
  const config = {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Don't set Content-Type for FormData (file uploads)
  if (options.body instanceof FormData) {
    delete config.headers['Content-Type'];
  }

  const response = await fetch(`${API_BASE}${url}`, config);
  return response;
}

// ----------------------------------------
// Auth
// ----------------------------------------
export async function login(username, password) {
  const res = await request('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
  return { ok: res.ok, data: await res.json() };
}

export async function logout() {
  const res = await request('/logout', { method: 'POST' });
  return { ok: res.ok, data: await res.json() };
}

export async function checkAuthStatus() {
  const res = await request('/auth/status');
  return { ok: res.ok, data: await res.json() };
}

// ----------------------------------------
// Sales CRUD
// ----------------------------------------
export async function getSales() {
  const res = await request('/sales');
  return { ok: res.ok, data: await res.json() };
}

export async function addSale(saleData) {
  const res = await request('/sales', {
    method: 'POST',
    body: JSON.stringify(saleData),
  });
  return { ok: res.ok, data: await res.json() };
}

export async function updateSale(id, saleData) {
  const res = await request(`/sales/${id}`, {
    method: 'PUT',
    body: JSON.stringify(saleData),
  });
  return { ok: res.ok, data: await res.json() };
}

export async function deleteSale(id) {
  const res = await request(`/sales/${id}`, { method: 'DELETE' });
  return { ok: res.ok, data: await res.json() };
}

export async function searchSales(product) {
  const res = await request(`/sales/search?product=${encodeURIComponent(product)}`);
  return { ok: res.ok, data: await res.json() };
}

// ----------------------------------------
// Dashboard Stats
// ----------------------------------------
export async function getStats() {
  const res = await request('/stats');
  return { ok: res.ok, data: await res.json() };
}

// ----------------------------------------
// Dataset
// ----------------------------------------
export async function getDataset() {
  const res = await request('/dataset');
  return { ok: res.ok, data: await res.json() };
}

// ----------------------------------------
// AI Prediction & Training
// ----------------------------------------
export async function predictSales(month) {
  const res = await request('/predict', {
    method: 'POST',
    body: JSON.stringify({ month: parseInt(month) }),
  });
  return { ok: res.ok, data: await res.json() };
}

export async function getModelInfo() {
  const res = await request('/model/info');
  return { ok: res.ok, data: await res.json() };
}

export async function getTrainStatus() {
  const res = await request('/train/status');
  return { ok: res.ok, data: await res.json() };
}

export async function trainModel() {
  const res = await request('/train', { method: 'POST' });
  return { ok: res.ok, data: await res.json() };
}

// ----------------------------------------
// CSV Upload
// ----------------------------------------
export async function uploadCSV(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await request('/upload-csv', {
    method: 'POST',
    body: formData,
  });
  return { ok: res.ok, data: await res.json() };
}

// ----------------------------------------
// Export URLs (direct downloads)
// ----------------------------------------
export const EXPORT_EXCEL_URL = `${API_BASE}/export/excel`;
export const EXPORT_PDF_URL = `${API_BASE}/export/pdf`;
