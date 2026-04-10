const API_BASE = import.meta.env.VITE_API_URL || '/api';

export async function submitComplaint(complainData) {
  try {
    const response = await fetch(`${API_BASE}/complaints/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(complainData)
    });
    const result = await response.json();
    if (response.ok) {
      saveLastComplaint(result);
    }
    return result;
  } catch (error) {
    console.error('Error submitting complaint:', error);
    return { error: 'Failed to submit complaint' };
  }
}

export async function fetchComplaintByRef(refId) {
  try {
    const response = await fetch(`${API_BASE}/complaints/${refId}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching complaint:', error);
    return null;
  }
}

export async function fetchAllComplaints(page = 1, filters = {}) {
  try {
    const params = new URLSearchParams({ page, ...filters });
    const response = await fetch(`${API_BASE}/admin/complaints?${params}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching complaints:', error);
    return { complaints: [] };
  }
}

export async function updateComplaintStatus(complaintId, status, notes = '') {
  try {
    const response = await fetch(`${API_BASE}/complaints/${complaintId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, resolution_notes: notes })
    });
    return await response.json();
  } catch (error) {
    console.error('Error updating complaint:', error);
    return { error: 'Failed to update complaint' };
  }
}

export async function getDashboardStats() {
  try {
    const response = await fetch(`${API_BASE}/admin/dashboard`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching dashboard stats:', error);
    return {
      total: 0,
      high_priority: 0,
      new: 0,
      in_progress: 0,
      resolved: 0,
      categories: {}
    };
  }
}

export async function classifyComplaint(text) {
  try {
    const response = await fetch(`${API_BASE}/classify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    return await response.json();
  } catch (error) {
    console.error('Error classifying complaint:', error);
    return { category: 'Public Services', department: 'Public Services Office', priority: 'Normal' };
  }
}

// Local storage fallbacks
const STORAGE_KEY = 'civicflowComplaints';
const LAST_KEY = 'civicflowLastComplaint';

export function saveLastComplaint(item) {
  localStorage.setItem(LAST_KEY, JSON.stringify(item));
}

export function loadLastComplaint() {
  const saved = localStorage.getItem(LAST_KEY);
  return saved ? JSON.parse(saved) : null;
}
