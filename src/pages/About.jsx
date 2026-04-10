export default function About() {
  return (
    <section className="about-section">
      <div className="container section-card">
        <div className="section-header">
          <p className="eyebrow">About the system</p>
          <h2>Streamlining public grievance management with smarter routing.</h2>
        </div>
        <div className="about-grid">
          <article>
            <h3>Purpose</h3>
            <p>Provide a unified interface for citizens and administrators to manage complaints with clarity and speed.</p>
          </article>
          <article>
            <h3>Capabilities</h3>
            <ul>
              <li>Complaint classification</li>
              <li>Rich metadata capture</li>
              <li>Status management</li>
              <li>Dashboard analytics</li>
            </ul>
          </article>
          <article>
            <h3>Vision</h3>
            <p>Help public service teams respond faster and keep citizens informed about issue progress.</p>
          </article>
        </div>
      </div>
    </section>
  );
}
