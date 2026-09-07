import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { Department } from '../../types';
import { Building2, Users, Ticket, Plus } from 'lucide-react';

export const DepartmentListPage: React.FC = () => {
  const [departments, setDepartments] = useState<Department[]>([]);

  useEffect(() => {
    apiFetch<Department[]>('/departments')
      .then((data) => setDepartments(data || []))
      .catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary tracking-tight">Department Management</h1>
          <p className="text-xs text-text-secondary mt-0.5">
            Organize support teams, department leads, and workload routing rules
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {departments.map((d) => (
          <div key={d.id} className="bg-surface p-5 rounded-2xl border border-border shadow-card space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 rounded-xl bg-brand-50 text-brand-600 font-bold text-sm">
                  {d.code}
                </div>
                <div>
                  <h3 className="text-sm font-bold text-text-primary">{d.name}</h3>
                  <p className="text-xs text-text-tertiary">Manager: {d.manager_name || 'Unassigned'}</p>
                </div>
              </div>
            </div>

            <p className="text-xs text-text-secondary line-clamp-2">{d.description}</p>

            <div className="grid grid-cols-2 gap-2 pt-3 border-t border-border text-center text-xs">
              <div className="p-2 bg-surface-subtle rounded-xl">
                <span className="text-[10px] uppercase font-bold text-text-tertiary">Members</span>
                <p className="text-sm font-bold text-text-primary mt-0.5">{d.member_count}</p>
              </div>
              <div className="p-2 bg-surface-subtle rounded-xl">
                <span className="text-[10px] uppercase font-bold text-text-tertiary">Open Tickets</span>
                <p className="text-sm font-bold text-brand-600 mt-0.5">{d.open_ticket_count}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
