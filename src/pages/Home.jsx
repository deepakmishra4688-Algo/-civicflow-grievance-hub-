import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <section className="hero-section">
      <div className="container hero-grid">
        <div className="hero-copy">
          <span className="eyebrow">Civic service coordination</span>
          <h2>Fast, reliable routing for citizen grievances.</h2>
          <p>
            Submit issues once, let the system classify them automatically, and monitor progress from the dashboard.
          </p>
          <Link className="button button-primary" to="/submit">
            File a New Complaint
          </Link>
        </div>
        <div className="hero-card">
          <div className="status-pill">CivicFlow Grievance Hub</div>
          <h3>How it works</h3>
          <ul>
            <li>Citizen registers a complaint</li>
            <li>AI classifies and assigns department</li>
            <li>Admin tracks status and trends</li>
          </ul>
        </div>
      </div>
      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <p className="eyebrow">Benefits</p>
            <h2>Clear complaint flow, less delay, better accountability.</h2>
          </div>
          <div className="feature-grid">
            <article className="feature-card">
              <h3>Automatic routing</h3>
              <p>Complaints are categorized and sent to the right division.</p>
            </article>
            <article className="feature-card">
              <h3>Priority handling</h3>
              <p>Urgent matters are marked high and easy to spot.</p>
            </article>
            <article className="feature-card">
              <h3>Trend visibility</h3>
              <p>See how issues are distributed across departments.</p>
            </article>
          </div>
        </div>
      </section>
    </section>
  );
}
