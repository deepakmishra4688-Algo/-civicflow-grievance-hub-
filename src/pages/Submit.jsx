import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { submitComplaint, classifyComplaint } from '../utils/complaints.js';

const initialForm = {
  name: '',
  phone: '',
  email: '',
  language: 'English',
  location: '',
  complaint: '',
  attachments: []
};

export default function Submit() {
  const [form, setForm] = useState(initialForm);
  const [files, setFiles] = useState([]);
  const [feedback, setFeedback] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleFileChange = (event) => {
    const fileList = Array.from(event.target.files);
    setFiles(fileList);
    setForm((current) => ({ ...current, attachments: fileList.map((file) => file.name) }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!form.name || !form.phone || !form.location || !form.complaint) {
      setFeedback('Please complete all required fields.');
      return;
    }

    setLoading(true);
    try {
      const result = await submitComplaint({
        name: form.name,
        phone: form.phone,
        email: form.email,
        language: form.language,
        location: form.location,
        complaint_text: form.complaint,
        attachments: form.attachments
      });

      if (result.success || result.ref_id) {
        setFeedback('Complaint submitted successfully. Redirecting to result...');
        setTimeout(() => navigate('/result'), 800);
      } else {
        setFeedback(result.error || 'Failed to submit complaint');
      }
    } catch (error) {
      setFeedback('Error submitting complaint');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="form-section">
      <div className="container section-card">
        <div className="section-header">
          <p className="eyebrow">Citizen Interface</p>
          <h2>Submit your grievance with location and attachments.</h2>
        </div>
        <form className="complaint-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <label htmlFor="name">Name</label>
            <input id="name" name="name" value={form.name} onChange={handleChange} placeholder="Enter full name" required />
          </div>
          <div className="form-row">
            <label htmlFor="phone">Phone Number</label>
            <input id="phone" name="phone" value={form.phone} onChange={handleChange} type="tel" placeholder="Enter phone number" required />
          </div>
          <div className="form-row">
            <label htmlFor="email">Email (Optional)</label>
            <input id="email" name="email" value={form.email} onChange={handleChange} type="email" placeholder="Enter email" />
          </div>
          <div className="form-row">
            <label htmlFor="language">Language</label>
            <select id="language" name="language" value={form.language} onChange={handleChange}>
              <option value="English">English</option>
              <option value="Hindi">Hindi</option>
              <option value="Regional">Regional</option>
            </select>
          </div>
          <div className="form-row">
            <label htmlFor="location">Location</label>
            <input id="location" name="location" value={form.location} onChange={handleChange} placeholder="Enter location or ward" required />
          </div>
          <div className="form-row full-width">
            <label htmlFor="complaint">Complaint Description</label>
            <textarea id="complaint" name="complaint" rows="6" value={form.complaint} onChange={handleChange} placeholder="Describe the issue" required />
          </div>
          <div className="form-row full-width">
            <label htmlFor="attachments">Attach documents / image / PDF</label>
            <input id="attachments" type="file" multiple accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.txt" onChange={handleFileChange} />
            {files.length > 0 && (
              <p className="attachment-note">Attached: {files.map((file) => file.name).join(', ')}</p>
            )}
          </div>
          <button type="submit" className="button button-primary" disabled={loading}>
            {loading ? 'Submitting...' : 'Submit Complaint'}
          </button>
          {feedback && <p className={`feedback-text ${feedback.includes('Error') ? 'error' : 'success'}`}>{feedback}</p>}
        </form>
      </div>
    </section>
  );
}
