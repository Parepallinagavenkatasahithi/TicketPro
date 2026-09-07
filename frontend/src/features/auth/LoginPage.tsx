import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Ticket, Lock, Mail, AlertCircle, ArrowRight } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('admin@ticketpro.internal');
  const [password, setPassword] = useState('Password123!');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = (roleEmail: string) => {
    setEmail(roleEmail);
    setPassword('Password123!');
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="w-14 h-14 rounded-2xl bg-brand text-white flex items-center justify-center mx-auto shadow-lg mb-4">
          <Ticket className="w-8 h-8" />
        </div>
        <h2 className="text-3xl font-bold tracking-tight text-text-primary">Sign in to TicketPro</h2>
        <p className="mt-2 text-sm text-text-secondary">Employee Ticket Management & IT Service Operations Platform</p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-surface py-8 px-6 shadow-card rounded-2xl border border-border sm:px-10">
          {error && (
            <div className="mb-4 p-3 rounded-xl bg-danger-light border border-danger/30 text-danger-dark text-xs flex items-center">
              <AlertCircle className="w-4 h-4 mr-2 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1">
                Corporate Email Address
              </label>
              <div className="relative rounded-xl shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-4 w-4 text-text-tertiary" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2.5 bg-surface-subtle border border-border rounded-xl text-sm focus:outline-none focus:border-brand"
                  placeholder="name@company.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1">
                Password
              </label>
              <div className="relative rounded-xl shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-4 w-4 text-text-tertiary" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2.5 bg-surface-subtle border border-border rounded-xl text-sm focus:outline-none focus:border-brand"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-semibold text-white bg-brand hover:bg-brand-600 focus:outline-none transition-colors"
            >
              {loading ? 'Authenticating...' : 'Sign In'}
              {!loading && <ArrowRight className="w-4 h-4 ml-2" />}
            </button>
          </form>

          {/* Demo Credentials Helper */}
          <div className="mt-6 pt-6 border-t border-border">
            <p className="text-[11px] font-bold uppercase tracking-wider text-text-tertiary text-center mb-3">
              Demo Credentials (Click to Select)
            </p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                type="button"
                onClick={() => handleQuickLogin('admin@ticketpro.internal')}
                className="p-2 rounded-lg bg-surface-subtle border border-border text-left hover:border-brand-300"
              >
                <div className="font-bold text-text-primary">Admin</div>
                <div className="text-[10px] text-text-tertiary truncate">admin@ticketpro.internal</div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('agent.alex@ticketpro.internal')}
                className="p-2 rounded-lg bg-surface-subtle border border-border text-left hover:border-brand-300"
              >
                <div className="font-bold text-text-primary">Support Agent</div>
                <div className="text-[10px] text-text-tertiary truncate">agent.alex@...</div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('it.manager@ticketpro.internal')}
                className="p-2 rounded-lg bg-surface-subtle border border-border text-left hover:border-brand-300"
              >
                <div className="font-bold text-text-primary">Manager</div>
                <div className="text-[10px] text-text-tertiary truncate">it.manager@...</div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('rohit.sharma@ticketpro.internal')}
                className="p-2 rounded-lg bg-surface-subtle border border-border text-left hover:border-brand-300"
              >
                <div className="font-bold text-text-primary">Employee</div>
                <div className="text-[10px] text-text-tertiary truncate">rohit.sharma@...</div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
