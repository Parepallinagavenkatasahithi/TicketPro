import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Ticket as TicketIcon, User as UserIcon, BookOpen, X } from 'lucide-react';
import { apiFetch } from '../../services/api';
import { Ticket, User, KBArticle } from '../../types';

interface GlobalSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const GlobalSearchModal: React.FC<GlobalSearchModalProps> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [kbArticles, setKbArticles] = useState<KBArticle[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else {
          // Open search modal
          const searchBtn = document.getElementById('global-search-trigger');
          if (searchBtn) searchBtn.click();
        }
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  useEffect(() => {
    if (!query.trim() || query.length < 2) {
      setTickets([]);
      setUsers([]);
      setKbArticles([]);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      try {
        const [tRes, uRes, kbRes] = await Promise.all([
          apiFetch<Ticket[]>(`/tickets?search=${encodeURIComponent(query)}&limit=5`),
          apiFetch<User[]>(`/users?search=${encodeURIComponent(query)}`),
          apiFetch<KBArticle[]>(`/knowledge-base?search=${encodeURIComponent(query)}&limit=3`),
        ]);
        setTickets(tRes || []);
        setUsers(uRes || []);
        setKbArticles(kbRes || []);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-text-primary/40 backdrop-blur-sm p-4 sm:p-6 md:p-20">
      <div className="mx-auto max-w-2xl transform overflow-hidden rounded-2xl bg-surface shadow-2xl transition-all border border-border">
        {/* Search Header */}
        <div className="relative flex items-center border-b border-border px-4 py-3">
          <Search className="w-5 h-5 text-text-tertiary mr-3" />
          <input
            type="text"
            className="w-full bg-transparent text-sm text-text-primary placeholder-text-tertiary focus:outline-none"
            placeholder="Search tickets, employees, departments, knowledge base... (Esc to close)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
          <button onClick={onClose} className="p-1 rounded-md text-text-tertiary hover:text-text-primary">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search Results */}
        <div className="max-h-96 overflow-y-auto p-4 space-y-4">
          {isLoading && (
            <div className="py-6 text-center text-xs text-text-tertiary">Searching TicketPro database...</div>
          )}

          {!isLoading && query && tickets.length === 0 && users.length === 0 && kbArticles.length === 0 && (
            <div className="py-6 text-center text-xs text-text-tertiary">No matching tickets or records found</div>
          )}

          {/* Tickets Section */}
          {tickets.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-text-tertiary uppercase tracking-wider mb-2">Tickets</div>
              <div className="space-y-1">
                {tickets.map((t) => (
                  <div
                    key={t.id}
                    onClick={() => {
                      navigate(`/tickets/${t.id}`);
                      onClose();
                    }}
                    className="flex items-center justify-between p-2.5 rounded-lg hover:bg-surface-subtle cursor-pointer"
                  >
                    <div className="flex items-center space-x-3">
                      <TicketIcon className="w-4 h-4 text-brand-500" />
                      <div>
                        <span className="text-xs font-bold text-brand-600 mr-2">{t.ticket_number}</span>
                        <span className="text-sm font-medium text-text-primary">{t.title}</span>
                      </div>
                    </div>
                    <span className="text-xs text-text-tertiary">{t.status}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Employees Section */}
          {users.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-text-tertiary uppercase tracking-wider mb-2">Employees</div>
              <div className="space-y-1">
                {users.map((u) => (
                  <div
                    key={u.id}
                    onClick={() => {
                      navigate(`/employees`);
                      onClose();
                    }}
                    className="flex items-center justify-between p-2.5 rounded-lg hover:bg-surface-subtle cursor-pointer"
                  >
                    <div className="flex items-center space-x-3">
                      <UserIcon className="w-4 h-4 text-info-dark" />
                      <div>
                        <span className="text-sm font-medium text-text-primary">{u.full_name}</span>
                        <span className="text-xs text-text-tertiary ml-2">({u.employee_id} • {u.job_title})</span>
                      </div>
                    </div>
                    <span className="text-xs font-semibold text-brand-600">{u.role_name}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* KB Articles Section */}
          {kbArticles.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-text-tertiary uppercase tracking-wider mb-2">Knowledge Base</div>
              <div className="space-y-1">
                {kbArticles.map((kb) => (
                  <div
                    key={kb.id}
                    onClick={() => {
                      navigate(`/knowledge-base/${kb.slug}`);
                      onClose();
                    }}
                    className="flex items-center justify-between p-2.5 rounded-lg hover:bg-surface-subtle cursor-pointer"
                  >
                    <div className="flex items-center space-x-3">
                      <BookOpen className="w-4 h-4 text-success-dark" />
                      <span className="text-sm font-medium text-text-primary">{kb.title}</span>
                    </div>
                    <span className="text-xs text-text-tertiary">{kb.view_count} views</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
