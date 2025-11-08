import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

export default function Login() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as any)?.from?.pathname || '/';

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      localStorage.setItem('auth', 'true');
      navigate(from, { replace: true });
    }, 1000);
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="card w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-2">Login</h1>
        <p className="text-sm text-white/70 mb-6">Access the Marine Robotics control interface.</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm mb-1">Username</label>
            <input className="input w-full" placeholder="operator" />
          </div>
          <div>
            <label className="block text-sm mb-1">Password</label>
            <input type="password" className="input w-full" placeholder="••••••" />
          </div>
          <button disabled={loading} className="btn-primary w-full disabled:opacity-50">
            {loading ? 'Authenticating...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}
