import { useEffect, useState } from 'react';
import { fetchAllComplaints, getDashboardStats, updateComplaintStatus } from '../utils/complaints.js';

const filterOptions = ['All', 'New', 'In Progress', 'Resolved', 'High'];

function formatDate(value) {
  return new Date(value).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
}

export default function Admin() {
  const [filter, setFilter] = useState('All');
  const [complaints, setComplaints] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    high_priority: 0,
    new: 0,
    in_progress: 0,
    resolved: 0,
    categories: {}
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const dashboardData = await getDashboardStats();
      setStats(dashboardData);
      
      const filterParams = {};
      if (filter !== 'All' && filter !== 'High') {
        filterParams.status = filter;
      } else if (filter === 'High') {
        filterParams.priority = 'High';
      }
      
      const complaintsData = await fetchAllComplaints(1, filterParams);
      setComplaints(complaintsData.complaints || []);
      setLoading(false);
    }
    loadData();
  }, [filter]);

  const handleStatusChange = async (complaintId, newStatus) => {
    await updateComplaintStatus(complaintId, newStatus);
    setFilter(filter); // Refresh data
  };

  const maxCategory = Math.max(...Object.values(stats.categories || {}), 1);

  return (
    <section className="dashboard-section">
      <div className="container section-card">
        <div className="section-header">
          <p className="eyebrow">Admin Dashboard</p>
          <h2>Track complaints and monitor priority flow.</h2>
        </div>
        
        <div className="stats-grid">
          <article className="stat-card">
            <p>Total Complaints</p>
            <h3>{stats.total}</h3>
          </article>
          <article className="stat-card">
            <p>High Priority</p>
            <h3>{stats.high_priority}</h3>
          </article>
          <article className="stat-card">
            <p>Active Departments</p>
            <h3>{Object.keys(stats.categories || {}).length}</h3>
          </article>
        </div>

        <div className="status-controls">
          {filterOptions.map((option) => (
            <button
              key={option}
              className={`button button-secondary status-filter ${filter === option ? 'active' : ''}`}
              onClick={() => setFilter(option)}
            >
              {option}
            </button>
          ))}
        </div>

        <div className="status-grid">
          <article className="stat-card">
            <p>New</p>
            <h3>{stats.new}</h3>
          </article>
          <article className="stat-card">
            <p>In Progress</p>
            <h3>{stats.in_progress}</h3>
          </article>
          <article className="stat-card">
            <p>Resolved</p>
            <h3>{stats.resolved}</h3>
          </article>
          <article className="stat-card">
            <p>High Priority</p>
            <h3>{stats.high_priority}</h3>
          </article>
        </div>

        <div className="table-section">
          <h3>Recent Complaints</h3>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Ref ID</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {complaints.length === 0 ? (
                    <tr>
                      <td colSpan="6" style={{ textAlign: 'center', color: 'var(--muted)' }}>
                        No complaints match this filter.
                      </td>
                    </tr>
                  ) : (
                    complaints.map((item) => (
                      <tr key={item.id}>
                        <td>{item.ref_id}</td>
                        <td>{item.category}</td>
                        <td>{item.complaint_text?.length > 60 ? `${item.complaint_text.slice(0, 57)}...` : item.complaint_text}</td>
                        <td>{item.location}</td>
                        <td>
                          <select 
                            value={item.status} 
                            onChange={(e) => handleStatusChange(item.id, e.target.value)}
                            style={{ padding: '0.5rem', borderRadius: '4px' }}
                          >
                            <option value="New">New</option>
                            <option value="In Progress">In Progress</option>
                            <option value="Resolved">Resolved</option>
                          </select>
                        </td>
                        <td>{formatDate(item.created_at)}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="trends-section">
          <h3>Department Trend</h3>
          {Object.entries(stats.categories || {}).map(([category, value]) => (
            <div className="trend-bar" key={category}>
              <label>{category}</label>
              <div className="bar"><span style={{ width: `${(value / maxCategory) * 100}%` }} /></div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
