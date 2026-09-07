import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, RoleName } from '../types';
import { apiFetch } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
  hasPermission: (permission: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const cached = localStorage.getItem('ticketpro_user');
    return cached ? JSON.parse(cached) : null;
  });
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('ticketpro_token'));
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchMe = async () => {
      if (!token) {
        setIsLoading(false);
        return;
      }
      try {
        const me = await apiFetch<User>('/auth/me');
        setUser(me);
        localStorage.setItem('ticketpro_user', JSON.stringify(me));
      } catch (err) {
        logout();
      } finally {
        setIsLoading(false);
      }
    };
    fetchMe();
  }, [token]);

  const login = async (email: string, password: string) => {
    const res = await apiFetch<{ access_token: string; user: User }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    setToken(res.access_token);
    setUser(res.user);
    localStorage.setItem('ticketpro_token', res.access_token);
    localStorage.setItem('ticketpro_user', JSON.stringify(res.user));
  };

  const register = async (data: any) => {
    await apiFetch('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('ticketpro_token');
    localStorage.removeItem('ticketpro_user');
  };

  const hasPermission = (permission: string): boolean => {
    if (!user) return false;
    if (user.role_name === 'ADMIN') return true;
    if (user.role_name === 'MANAGER') return !['settings.manage', 'audit.view'].includes(permission);
    if (user.role_name === 'AGENT') return ['ticket.create', 'ticket.view', 'ticket.edit', 'ticket.assign', 'ticket.resolve', 'ticket.comment', 'ticket.internal_note', 'kb.manage'].includes(permission);
    return ['ticket.create', 'ticket.view', 'ticket.comment', 'kb.view'].includes(permission);
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, register, logout, hasPermission }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
