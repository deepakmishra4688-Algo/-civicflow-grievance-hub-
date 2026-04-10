import { HashRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout.jsx';
import Home from './pages/Home.jsx';
import Submit from './pages/Submit.jsx';
import Result from './pages/Result.jsx';
import Admin from './pages/Admin.jsx';
import About from './pages/About.jsx';

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="submit" element={<Submit />} />
          <Route path="result" element={<Result />} />
          <Route path="admin" element={<Admin />} />
          <Route path="about" element={<About />} />
        </Route>
      </Routes>
    </HashRouter>
  );
}
