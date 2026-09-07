import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { User, Department } from '../../types';
import { Search, UserPlus, Shield, Mail, Building2, CheckCircle2, XCircle } from 'lucide-react';
import { formatDate } from '../../lib/utils';

export const EmployeeListPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [deptFilter, setDeptFilter] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const queryParts = [];
      if (search) queryParts.push(`search=${encodeURIComponent(search)}`);
      if (roleFilter) queryParts.push(`role=${encodeURIComponent(roleFilter)}`);
      if (deptFilter) queryParts.push(`department_id=${deptFilter}`);
      const qs = queryParts.length > 0 ? `?${queryParts.join('&')}` : '';

      const [uRes, dRes] = await Promise.all([
        apiFetch<User[]>(`/users${qs}`),
        apiFetch<Department[]>('/departments'),
      ]);
      setUsers(uRes || []);
      setDepartments(dRes || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [roleFilter, deptFilter]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-text-primary tracking-tight">Employee Directory</h1>
          <p className="text-xs text-text-secondary mt-0.5">
            Manage organization users, department assignments, and role permissions
          </p>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-surface p-4 rounded-2xl border border-border shadow-card flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-3 text-text-tertiary" />
          <input
            type="text"
            placeholder="Search by name, email, employee ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && fetchUsers()}
            className="w-full pl-9 pr-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs focus:outline-none focus:border-brand"
          />
        </div>

        <select
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value)}
          className="px-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs text-text-secondary focus:outline-none"
        >
          <option value="">All Roles</option>
          <option value="ADMIN">ADMIN</option>
          <option value="MANAGER">MANAGER</option>
          <option value="AGENT">AGENT</option>
          <option value="EMPLOYEE">EMPLOYEE</option>
        </select>

        <select
          value={deptFilter}
          onChange={(e) => setDeptFilter(e.target.value)}
          className="px-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs text-text-secondary focus:outline-none"
        >
          <option value="">All Departments</option>
          {departments.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name}
            </option>
          ))}
        </select>
      </div>

      {/* Employee Table */}
      <div className="bg-surface rounded-2xl border border-border shadow-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-surface-subtle border-b border-border text-text-tertiary font-semibold uppercase tracking-wider">
              <tr>
                <th className="px-5 py-3.5">Employee ID</th>
                <th className="px-5 py-3.5">Name & Job Title</th>
                <th className="px-5 py-3.5">Email</th>
                <th className="px-5 py-3.5">Department</th>
                <th className="px-5 py-3.5">Role</th>
                <th className="px-5 py-3.5">Status</th>
                <th className="px-5 py-3.5">Joined Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-text-primary">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-surface-subtle/80 transition-colors">
                  <td className="px-5 py-3.5 font-bold text-brand-600">{u.employee_id}</td>
                  <td className="px-5 py-3.5">
                    <div className="font-bold text-text-primary">{u.full_name}</div>
                    <div className="text-[10px] text-text-tertiary">{u.job_title || 'Employee'}</div>
                  </td>
                  <td className="px-5 py-3.5 text-text-secondary">{u.email}</td>
                  <td className="px-5 py-3.5">{u.department_name || 'IT'}</td>
                  <td className="px-5 py-3.5">
                    <span className="inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-bold bg-brand-50 text-brand-700 border border-brand-200">
                      {u.role_name}
                    </span>
                  </td>
                  <td className="px-5 py-3.5">
                    {u.is_active ? (
                      <span className="inline-flex items-center text-success-dark font-semibold">
                        <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Active
                      </span>
                    ) : (
                      <span className="inline-flex items-center text-danger-dark font-semibold">
                        <XCircle className="w-3.5 h-3.5 mr-1" /> Inactive
                      </span>
                    )}
                  </td>
                  <td className="px-5 py-3.5 text-text-tertiary">{formatDate(u.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
