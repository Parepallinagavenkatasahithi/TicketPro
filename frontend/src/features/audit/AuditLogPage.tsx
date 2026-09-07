import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { AuditLog } from '../../types';
import { History, Shield, Search } from 'lucide-react';
import { formatDate } from '../../lib/utils';

export const AuditLogPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);

  useEffect(() => {
    apiFetch<AuditLog[]>('/audit')
      .then((data) => setLogs(data || []))
      .catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary tracking-tight">Security Audit Logs</h1>
        <p className="text-xs text-text-secondary mt-0.5">
          Immutable audit trail recording security events, ticket state changes, and user actions
        </p>
      </div>

      <div className="bg-surface rounded-2xl border border-border shadow-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-surface-subtle border-b border-border text-text-tertiary font-semibold uppercase tracking-wider">
              <tr>
                <th className="px-5 py-3.5">Timestamp</th>
                <th className="px-5 py-3.5">Actor</th>
                <th className="px-5 py-3.5">Action</th>
                <th className="px-5 py-3.5">Resource Type</th>
                <th className="px-5 py-3.5">Resource ID</th>
                <th className="px-5 py-3.5">IP Address</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-text-primary">
              {logs.map((l) => (
                <tr key={l.id} className="hover:bg-surface-subtle/80 transition-colors">
                  <td className="px-5 py-3.5 font-medium text-text-secondary">{formatDate(l.created_at)}</td>
                  <td className="px-5 py-3.5 font-bold text-text-primary">{l.actor_name || 'System'}</td>
                  <td className="px-5 py-3.5">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-brand-50 text-brand-700 border border-brand-200">
                      {l.action}
                    </span>
                  </td>
                  <td className="px-5 py-3.5 font-semibold text-text-secondary">{l.resource_type}</td>
                  <td className="px-5 py-3.5 font-bold text-brand-600">{l.resource_id || 'N/A'}</td>
                  <td className="px-5 py-3.5 text-text-tertiary">{l.ip_address || '127.0.0.1'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
