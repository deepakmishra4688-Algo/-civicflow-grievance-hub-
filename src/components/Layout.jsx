import { Link, Outlet } from 'react-router-dom';
import Chatbot from './Chatbot.jsx';

const navItems = [
  { label: 'Home', path: '/' },
  { label: 'Submit', path: '/submit' },
  { label: 'Admin', path: '/admin' },
  { label: 'About', path: '/about' }
];

export default function Layout() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="container nav-container">
          <div className="brand">
            <div className="brand-mark">C</div>
            <div>
              <h1>CivicFlow Grievance Hub</h1>
              <p>Fast routing, clear status, better citizen service.</p>
            </div>
          </div>
          <nav className="nav-links">
            {navItems.map((item) => (
              <Link key={item.path} to={item.path} className="nav-link">
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>

      <main>
        <Outlet />
      </main>

      <Chatbot />

      <footer className="footer">
        <div className="container footer-content">
          <p>© 2026 CivicFlow Grievance Hub. Designed for streamlined civic service coordination.</p>
        </div>
      </footer>
    </div>
  );
}
