import { NavLink } from 'react-router-dom';

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `px-3 py-2 rounded-lg transition block ${isActive ? 'bg-ocean-600 text-white' : 'text-white/85 hover:bg-white/10'}`;

export default function Sidebar() {
  return (
    <aside className="hidden md:flex md:w-64 border-r border-white/10 bg-white/5 backdrop-blur">
      <div className="p-4 w-full">
        <div className="text-white/70 text-xs uppercase tracking-widest mb-3">Navigation</div>
        <nav className="space-y-1">
          <NavLink to="/" className={linkClass}>Welcome</NavLink>
          <NavLink to="/dashboard" className={linkClass}>Dashboard</NavLink>
          <NavLink to="/manual-control" className={linkClass}>Manual Control</NavLink>
          <NavLink to="/education" className={linkClass}>Education</NavLink>
        </nav>
      </div>
    </aside>
  );
}
