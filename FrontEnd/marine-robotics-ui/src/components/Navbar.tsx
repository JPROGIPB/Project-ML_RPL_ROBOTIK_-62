import { Link, useNavigate } from 'react-router-dom';
import { useMemo } from 'react';

export default function Navbar() {
  const navigate = useNavigate();
  const authed = useMemo(() => localStorage.getItem('auth') === 'true', []);

  function handleLogout() {
    localStorage.removeItem('auth');
    navigate('/login', { replace: true });
  }
  return (
    <header className="border-b border-white/10 bg-white/5 backdrop-blur sticky top-0 z-10">
      <div className="container-page flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-ocean-500 flex items-center justify-center font-bold">MR</div>
          <div>
            <div className="text-lg font-semibold">Marine Robotics</div>
            <div className="text-xs text-white/70">Ocean Technology UI Template</div>
          </div>
        </div>
        <nav className="hidden md:flex items-center gap-6 text-white/90">
          <Link to="/" className="hover:text-white">Welcome</Link>
          <Link to="/dashboard" className="hover:text-white">Dashboard</Link>
          <Link to="/manual-control" className="hover:text-white">Manual Control</Link>
          <Link to="/education" className="hover:text-white">Education</Link>
        </nav>
        <div className="flex items-center gap-2">
          {authed ? (
            <button onClick={handleLogout} className="btn-primary">Logout</button>
          ) : (
            <Link to="/login" className="btn-primary">Login</Link>
          )}
        </div>
      </div>
    </header>
  );
}
