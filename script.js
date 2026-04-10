const complaintForm = document.getElementById('complaintForm');
const resultSection = document.getElementById('result');
const resultCategory = document.getElementById('resultCategory');
const resultPriority = document.getElementById('resultPriority');
const resultDepartment = document.getElementById('resultDepartment');
const complaintTableBody = document.getElementById('complaintTableBody');
const statTotal = document.getElementById('statTotal');
const statHigh = document.getElementById('statHigh');
const statDepartments = document.getElementById('statDepartments');
const statusNew = document.getElementById('statusNew');
const statusInProgress = document.getElementById('statusInProgress');
const statusResolved = document.getElementById('statusResolved');
const statusHigh = document.getElementById('statusHigh');
const barElectricity = document.getElementById('barElectricity');
const barWater = document.getElementById('barWater');
const barSanitation = document.getElementById('barSanitation');
const barRoads = document.getElementById('barRoads');
const barPublicServices = document.getElementById('barPublicServices');
const chatToggle = document.getElementById('chatToggle');
const chatPanel = document.getElementById('chatPanel');
const chatClose = document.getElementById('chatClose');
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSend');

const categories = [
  { name: 'Electricity', department: 'Electrical Services' },
  { name: 'Water Supply', department: 'Water Department' },
  { name: 'Sanitation', department: 'Sanitation & Waste Management' },
  { name: 'Roads', department: 'Roads & Transport' },
  { name: 'Public Services', department: 'Public Services Office' }
];

const keywords = [
  { category: 'Electricity', terms: ['power', 'electricity', 'meter', 'light', 'breaker', 'transformer', 'outage', 'cable'] },
  { category: 'Water Supply', terms: ['water', 'pipeline', 'tap', 'leak', 'sewer', 'supply', 'borewell', 'tank'] },
  { category: 'Sanitation', terms: ['garbage', 'waste', 'drain', 'cleanliness', 'toilet', 'sewerage', 'dustbin', 'smell'] },
  { category: 'Roads', terms: ['pothole', 'road', 'street', 'traffic', 'drainage', 'sidewalk', 'bridge', 'junction'] },
  { category: 'Public Services', terms: ['bus', 'school', 'hospital', 'license', 'permit', 'ration', 'service', 'benefit'] }
];

const priorityWords = ['urgent', 'emergency', 'critical', 'danger', 'accident', 'flood', 'collapse', 'unsafe'];

function classifyComplaint(text) {
  const normalized = text.toLowerCase();
  let best = { category: 'Public Services', score: 0 };

  for (const rule of keywords) {
    let score = 0;
    for (const term of rule.terms) {
      if (normalized.includes(term)) score += 1;
    }
    if (score > best.score) {
      best = { category: rule.category, score };
    }
  }

  const category = best.category;
  const department = categories.find(item => item.name === category)?.department || 'Public Services Office';
  const urgentMatch = priorityWords.some(word => normalized.includes(word));
  const priority = urgentMatch ? 'High' : text.length > 120 ? 'Medium' : 'Normal';

  return { category, department, priority };
}

function loadComplaints() {
  const saved = localStorage.getItem('grievanceComplaints');
  return saved ? JSON.parse(saved) : [];
}

function saveComplaints(complaints) {
  localStorage.setItem('grievanceComplaints', JSON.stringify(complaints));
}

function formatDate(value) {
  return new Date(value).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
}

function getStatusCounts(complaints) {
  return {
    newCount: complaints.filter(item => item.status === 'New').length,
    progressCount: complaints.filter(item => item.status === 'In Progress').length,
    resolvedCount: complaints.filter(item => item.status === 'Resolved').length,
    highCount: complaints.filter(item => item.priority === 'High').length
  };
}

function renderDashboard(filter = 'All') {
  const complaints = loadComplaints();
  const totals = complaints.length;
  const highPriority = complaints.filter(item => item.priority === 'High').length;
  const departments = [...new Set(complaints.map(item => item.department))].length;
  const statusCounts = getStatusCounts(complaints);

  statTotal.textContent = totals;
  statHigh.textContent = highPriority;
  statDepartments.textContent = departments;
  statusNew.textContent = statusCounts.newCount;
  statusInProgress.textContent = statusCounts.progressCount;
  statusResolved.textContent = statusCounts.resolvedCount;
  statusHigh.textContent = statusCounts.highCount;

  const counts = {
    Electricity: 0,
    'Water Supply': 0,
    Sanitation: 0,
    Roads: 0,
    'Public Services': 0
  };

  complaints.forEach(item => {
    counts[item.category] = (counts[item.category] || 0) + 1;
  });

  const max = Math.max(...Object.values(counts), 1);
  barElectricity.style.width = `${(counts.Electricity / max) * 100}%`;
  barWater.style.width = `${(counts['Water Supply'] / max) * 100}%`;
  barSanitation.style.width = `${(counts.Sanitation / max) * 100}%`;
  barRoads.style.width = `${(counts.Roads / max) * 100}%`;
  barPublicServices.style.width = `${(counts['Public Services'] / max) * 100}%`;

  const filtered = complaints.filter(item => {
    if (filter === 'All') return true;
    if (filter === 'High') return item.priority === 'High';
    return item.status === filter;
  });

  complaintTableBody.innerHTML = '';
  const recent = [...filtered].reverse().slice(0, 12);
  if (recent.length === 0) {
    complaintTableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; color: var(--muted);">No complaints match this filter.</td></tr>`;
  } else {
    recent.forEach(item => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${item.id}</td>
        <td>${item.category}</td>
        <td>${item.complaint.length > 60 ? item.complaint.slice(0, 57) + '...' : item.complaint}</td>
        <td>${item.location}</td>
        <td>${item.status}</td>
        <td>${formatDate(item.submittedAt)}</td>
      `;
      complaintTableBody.appendChild(row);
    });
  }
}

function updateFilterButtons(selected) {
  document.querySelectorAll('.status-filter').forEach(button => {
    button.classList.toggle('active', button.dataset.status === selected);
  });
}

function showResult(result) {
  resultCategory.textContent = result.category;
  resultPriority.textContent = result.priority;
  resultDepartment.textContent = result.department;
  resultSection.classList.remove('hidden');
  resultSection.scrollIntoView({ behavior: 'smooth' });
}

function addChatMessage(content, type = 'bot') {
  const message = document.createElement('div');
  message.className = `chat-message ${type}`;
  message.textContent = content;
  chatBody.appendChild(message);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function getChatResponse(text) {
  const normalized = text.toLowerCase();
  if (normalized.includes('submit') || normalized.includes('complaint')) {
    return 'Use the complaint form to enter your name, phone, location, issue details and attach any supporting file. Then press Classify Complaint.';
  }
  if (normalized.includes('status') || normalized.includes('track')) {
    return 'You can track complaint status on the Admin Dashboard by checking New, In Progress, Resolved, or High Priority sections.';
  }
  if (normalized.includes('priority')) {
    return 'Priority is determined automatically by the complaint details. Urgent issues are marked High.';
  }
  if (normalized.includes('attachment') || normalized.includes('photo') || normalized.includes('pdf')) {
    return 'Attach images, PDFs, or documents in the attachment field before submitting the complaint.';
  }
  return 'I can help with complaint submission, tracking, and status. Try asking "How do I submit a complaint?" or "How do I track status?"';
}

complaintForm.addEventListener('submit', event => {
  event.preventDefault();
  const name = document.getElementById('name').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const language = document.getElementById('language').value;
  const location = document.getElementById('location').value.trim();
  const complaint = document.getElementById('complaint').value.trim();
  const attachmentFiles = Array.from(document.getElementById('attachments').files);

  if (!name || !phone || !location || !complaint) return;

  const classification = classifyComplaint(complaint);
  const attachments = attachmentFiles.map(file => file.name);
  const complaintRecord = {
    id: `CMP-${Date.now()}`,
    name,
    phone,
    language,
    location,
    complaint,
    category: classification.category,
    department: classification.department,
    priority: classification.priority,
    status: 'New',
    attachments,
    submittedAt: new Date().toISOString()
  };

  const complaints = loadComplaints();
  complaints.push(complaintRecord);
  saveComplaints(complaints);
  renderDashboard();
  showResult(classification);
  complaintForm.reset();
});

function initStatusControls() {
  document.querySelectorAll('.status-filter').forEach(button => {
    button.addEventListener('click', () => {
      const status = button.dataset.status;
      updateFilterButtons(status);
      renderDashboard(status);
    });
  });
}

chatToggle.addEventListener('click', () => {
  chatPanel.classList.toggle('hidden');
});

chatClose.addEventListener('click', () => {
  chatPanel.classList.add('hidden');
});

chatSend.addEventListener('click', () => {
  const text = chatInput.value.trim();
  if (!text) return;
  addChatMessage(text, 'user');
  chatInput.value = '';
  setTimeout(() => {
    addChatMessage(getChatResponse(text), 'bot');
  }, 350);
});

chatInput.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    event.preventDefault();
    chatSend.click();
  }
});

window.addEventListener('load', () => {
  chatPanel.classList.add('hidden');
  renderDashboard();
  initStatusControls();
});
