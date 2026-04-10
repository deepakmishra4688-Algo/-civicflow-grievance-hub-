import { loadLastComplaint } from '../utils/complaints.js';

function formatDate(value) {
  return new Date(value).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
}

export default function Result() {
  const complaint = loadLastComplaint();

  if (!complaint) {
    return (
      <section className="result-section">
        <div className="container section-card">
          <div className="section-header">
            <p className="eyebrow">Result</p>
            <h2>No complaint is available yet.</h2>
          </div>
          <p>Please submit a complaint first, then return to this page.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="result-section">
      <div className="container section-card">
        <div className="section-header">
          <p className="eyebrow">Classification Result</p>
          <h2>Your complaint has been routed successfully.</h2>
        </div>
        <div className="result-grid">
          <div className="result-card">
            <h3>Category</h3>
            <p>{complaint.category}</p>
          </div>
          <div className="result-card">
            <h3>Priority</h3>
            <p>{complaint.priority}</p>
          </div>
          <div className="result-card">
            <h3>Department</h3>
            <p>{complaint.department}</p>
          </div>
        </div>
        <div className="result-details">
          <div>
            <strong>Reference ID</strong>
            <p>{complaint.id}</p>
          </div>
          <div>
            <strong>Location</strong>
            <p>{complaint.location}</p>
          </div>
          <div>
            <strong>Date</strong>
            <p>{formatDate(complaint.submittedAt)}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
