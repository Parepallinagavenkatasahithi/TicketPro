import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Search, Bell, Menu, Sun, Moon, Check, Ticket, AlertTriangle } from 'lucide-react';
import { apiFetch } from '../../services/api';
import { NotificationItem } from '../../types';
import { formatTimeAgo } from '../../lib/utils';

interface HeaderProps {
  onToggleSidebar: () => void;
  onOpenSearch: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleSidebar, onOpenSearch }) => {
  const { user, logout } = useAuth();
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  useEffect(() => {
    const fetchNotifications = async () => {
      if (!user) return;
      try {
        const data = await apiFetch<NotificationItem[]>('/notifications?limit=10');
        setNotifications(data || []);
      } catch (err) {
        console.error('Error fetching notifications:', err);
      }
    };
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 30000);
    return () => clearInterval(interval);
  }, [user]);

  const unreadCount = notifications.filter(n => !n.is_read).length;

  const markAllRead = async () => {
    try {
      await apiFetch('/notifications/read-all', { method: 'PUT' });
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <header className="sticky top-0 z-30 bg-surface border-b border-border h-16 flex items-center justify-between px-4 sm:px-6 shadow-sm">
      {/* Left items */}
      <div className="flex items-center space-x-4">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg text-text-secondary hover:bg-surface-subtle hover:text-text-primary"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Global Search trigger */}
        <button
          id="global-search-trigger"
          onClick={onOpenSearch}
          className="hidden sm:flex items-center space-x-3 w-64 md:w-80 px-3.5 py-2 rounded-xl bg-surface-subtle border border-border text-text-tertiary text-sm hover:border-brand-300 transition-colors"
        >
          <Search className="w-4 h-4 text-text-tertiary" />
          <span className="flex-1 text-left truncate">Search tickets, employees...</span>
          <kbd className="px-1.5 py-0.5 text-[10px] font-semibold bg-surface rounded border border-border text-text-tertiary shadow-sm">
            ⌘K
          </kbd>
        </button>
      </div>

      {/* Right items */}
      <div className="flex items-center space-x-3">
        {/* Mobile Search Button */}
        <button
          onClick={onOpenSearch}
          className="sm:hidden p-2 rounded-lg text-text-secondary hover:bg-surface-subtle"
        >
          <Search className="w-5 h-5" />
        </button>

        {/* Notifications Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative p-2 rounded-lg text-text-secondary hover:bg-surface-subtle hover:text-text-primary transition-colors"
          >
            <Bell className="w-5 h-5" />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-4 h-4 rounded-full bg-danger text-white text-[10px] font-bold flex items-center justify-center animate-pulse">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-surface rounded-2xl shadow-dropdown border border-border p-4 z-50 animate-in fade-in slide-in-from-top-2">
              <div className="flex items-center justify-between border-b border-border pb-3 mb-3">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-sm text-text-primary">Notifications</span>
                  {unreadCount > 0 && (
                    <span className="bg-brand-50 text-brand-700 text-xs font-semibold px-2 py-0.5 rounded-full">
                      {unreadCount} new
                    </span>
                  )}
                </div>
                {unreadCount > 0 && (
                  <button
                    onClick={markAllRead}
                    className="text-xs text-brand-600 font-semibold hover:underline flex items-center"
                  >
                    <Check className="w-3.5 h-3.5 mr-1" /> Mark all read
                  </button>
                )}
              </div>

              <div className="max-h-72 overflow-y-auto space-y-2">
                {notifications.length === 0 ? (
                  <p className="text-xs text-text-tertiary text-center py-4">No recent notifications</p>
                ) : (
                  notifications.map((n) => (
                    <div
                      key={n.id}
                      className={`p-2.5 rounded-xl border text-xs transition-colors ${
                        n.is_read
                          ? 'bg-surface border-border text-text-secondary'
                          : 'bg-brand-50/50 border-brand-200 text-text-primary font-medium'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <span className="font-bold text-text-primary">{n.title}</span>
                        <span className="text-[10px] text-text-tertiary">{formatTimeAgo(n.created_at)}</span>
                      </div>
                      <p className="text-text-secondary mt-1 line-clamp-2">{n.message}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* User Avatar Menu */}
        <div className="relative">
          <button
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            className="flex items-center space-x-2 p-1 rounded-xl hover:bg-surface-subtle transition-colors"
          >
            <div className="w-9 h-9 rounded-full bg-brand-500 text-white font-bold flex items-center justify-center text-sm shadow-sm">
              {user?.full_name?.charAt(0) || 'U'}
            </div>
          </button>

          {showProfileMenu && (
            <div className="absolute right-0 mt-2 w-56 bg-surface rounded-2xl shadow-dropdown border border-border py-2 z-50">
              <div className="px-4 py-2 border-b border-border">
                <p className="text-sm font-bold text-text-primary">{user?.full_name}</p>
                <p className="text-xs text-text-tertiary">{user?.email}</p>
                <span className="inline-block mt-1 text-[10px] font-bold bg-brand-50 text-brand-700 px-2 py-0.5 rounded-full uppercase">
                  {user?.role_name}
                </span>
              </div>
              <button
                onClick={() => {
                  setShowProfileMenu(false);
                  logout();
                }}
                className="w-full text-left px-4 py-2.5 text-xs font-semibold text-danger hover:bg-danger-light transition-colors"
              >
                Sign out of TicketPro
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
