import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { apiFetch } from '../../services/api';
import { Ticket, TicketCategory, Department, User } from '../../types';
import { TicketStatusBadge } from '../../components/ui/TicketStatusBadge';
import { PriorityBadge } from '../../components/ui/PriorityBadge';
import { SLABadge } from '../../components/ui/SLABadge';
import {
  Search, Filter, LayoutGrid, List, PlusCircle, RefreshCw, CheckSquare
} from 'lucide-react';
import { formatTimeAgo } from '../../lib/utils';

export const TicketListPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [categories, setCategories] = useState<TicketCategory[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [agents, setAgents] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'table' | 'kanban'>('table');

  // Filter state
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [status, setStatus] = useState(searchParams.get('status') || '');
  const [priority, setPriority] = useState(searchParams.get('priority') || '');
  const [categoryId, setCategoryId] = useState(searchParams.get('category_id') || '');
  const [departmentId, setDepartmentId] = useState(searchParams.get('department_id') || '');

  const navigate = useNavigate();

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const queryParts = [];
      if (search) queryParts.push(`search=${encodeURIComponent(search)}`);
      if (status) queryParts.push(`status=${encodeURIComponent(status)}`);
      if (priority) queryParts.push(`priority=${encodeURIComponent(priority)}`);
      if (categoryId) queryParts.push(`category_id=${categoryId}`);
      if (departmentId) queryParts.push(`department_id=${departmentId}`);

      const queryString = queryParts.length > 0 ? `?${queryParts.join('&')}` : '';

      const [tRes, cRes, dRes, uRes] = await Promise.all([
        apiFetch<Ticket[]>(`/tickets${queryString}`),
        apiFetch<TicketCategory[]>('/tickets/categories'),
        apiFetch<Department[]>('/departments'),
        apiFetch<User[]>('/users?role=AGENT'),
      ]);

      setTickets(tRes || []);
      setCategories(cRes || []);
      setDepartments(dRes || []);
      setAgents(uRes || []);
    } catch (err) {
      console.error('Error fetching tickets:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, [status, priority, categoryId, departmentId]);

  const kanbanColumns = ['NEW', 'OPEN', 'ASSIGNED', 'IN_PROGRESS', 'WAITING_FOR_USER', 'RESOLVED'];

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-text-primary tracking-tight">Support Ticket Queue</h1>
          <p className="text-xs text-text-secondary mt-0.5">
            Manage, assign, and resolve enterprise support tickets across departments
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center bg-surface border border-border rounded-xl p-1 shadow-sm">
            <button
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded-lg text-xs font-semibold flex items-center ${
                viewMode === 'table' ? 'bg-brand text-white' : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              <List className="w-4 h-4 mr-1" /> Table
            </button>
            <button
              onClick={() => setViewMode('kanban')}
              className={`p-1.5 rounded-lg text-xs font-semibold flex items-center ${
                viewMode === 'kanban' ? 'bg-brand text-white' : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              <LayoutGrid className="w-4 h-4 mr-1" /> Kanban
            </button>
          </div>

          <button
            onClick={fetchTickets}
            className="p-2.5 rounded-xl bg-surface border border-border text-text-secondary hover:text-text-primary shadow-sm"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Filter Toolbar (Section 55) */}
      <div className="bg-surface p-4 rounded-2xl border border-border shadow-card space-y-3">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
          {/* Search Box */}
          <div className="relative md:col-span-1">
            <Search className="w-4 h-4 absolute left-3 top-3 text-text-tertiary" />
            <input
              type="text"
              placeholder="Search ID, title, desc..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && fetchTickets()}
              className="w-full pl-9 pr-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs focus:outline-none focus:border-brand"
            />
          </div>

          {/* Status Filter */}
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="px-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs text-text-secondary focus:outline-none"
          >
            <option value="">All Statuses</option>
            <option value="NEW">New</option>
            <option value="OPEN">Open</option>
            <option value="ASSIGNED">Assigned</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="WAITING_FOR_USER">Waiting for User</option>
            <option value="RESOLVED">Resolved</option>
            <option value="CLOSED">Closed</option>
          </select>

          {/* Priority Filter */}
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="px-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs text-text-secondary focus:outline-none"
          >
            <option value="">All Priorities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>

          {/* Category Filter */}
          <select
            value={categoryId}
            onChange={(e) => setCategoryId(e.target.value)}
            className="px-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs text-text-secondary focus:outline-none"
          >
            <option value="">All Categories</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>

          {/* Department Filter */}
          <select
            value={departmentId}
            onChange={(e) => setDepartmentId(e.target.value)}
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
      </div>

      {/* Main Ticket Views */}
      {viewMode === 'table' ? (
        /* Table View (Section 52) */
        <div className="bg-surface rounded-2xl border border-border shadow-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-surface-subtle border-b border-border text-text-tertiary font-semibold uppercase tracking-wider">
                <tr>
                  <th className="px-5 py-3.5">Ticket ID</th>
                  <th className="px-5 py-3.5">Subject</th>
                  <th className="px-5 py-3.5">Requester</th>
                  <th className="px-5 py-3.5">Department</th>
                  <th className="px-5 py-3.5">Priority</th>
                  <th className="px-5 py-3.5">Status</th>
                  <th className="px-5 py-3.5">Assignee</th>
                  <th className="px-5 py-3.5">SLA Countdown</th>
                  <th className="px-5 py-3.5">Updated</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-text-primary">
                {tickets.length === 0 ? (
                  <tr>
                    <td colSpan={9} className="px-5 py-12 text-center text-text-tertiary">
                      No tickets found matching your filter criteria.
                    </td>
                  </tr>
                ) : (
                  tickets.map((t) => (
                    <tr
                      key={t.id}
                      onClick={() => navigate(`/tickets/${t.id}`)}
                      className="hover:bg-surface-subtle/80 cursor-pointer transition-colors"
                    >
                      <td className="px-5 py-3.5 font-bold text-brand-600">{t.ticket_number}</td>
                      <td className="px-5 py-3.5 font-medium max-w-xs truncate">{t.title}</td>
                      <td className="px-5 py-3.5">{t.requester_name || 'Employee'}</td>
                      <td className="px-5 py-3.5 text-text-secondary">{t.department_name || 'IT'}</td>
                      <td className="px-5 py-3.5">
                        <PriorityBadge priority={t.priority} />
                      </td>
                      <td className="px-5 py-3.5">
                        <TicketStatusBadge status={t.status} />
                      </td>
                      <td className="px-5 py-3.5 text-text-secondary">{t.assigned_agent_name || 'Unassigned'}</td>
                      <td className="px-5 py-3.5">
                        <SLABadge targetDate={t.resolution_due_at} isBreached={t.is_overdue} />
                      </td>
                      <td className="px-5 py-3.5 text-text-tertiary">{formatTimeAgo(t.updated_at)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        /* Kanban View (Section 53) */
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 overflow-x-auto pb-4">
          {kanbanColumns.map((colStatus) => {
            const colTickets = tickets.filter((t) => t.status === colStatus);
            return (
              <div key={colStatus} className="bg-surface-subtle p-3 rounded-2xl border border-border flex flex-col min-w-[240px]">
                <div className="flex items-center justify-between mb-3 px-1">
                  <span className="text-xs font-bold uppercase tracking-wider text-text-secondary">{colStatus.replace('_', ' ')}</span>
                  <span className="text-xs font-semibold bg-surface px-2 py-0.5 rounded-full text-text-tertiary border border-border">
                    {colTickets.length}
                  </span>
                </div>

                <div className="space-y-3 flex-1 overflow-y-auto max-h-[calc(100vh-320px)]">
                  {colTickets.map((t) => (
                    <div
                      key={t.id}
                      onClick={() => navigate(`/tickets/${t.id}`)}
                      className="bg-surface p-3.5 rounded-xl border border-border shadow-sm hover:shadow-card cursor-pointer space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-brand-600">{t.ticket_number}</span>
                        <PriorityBadge priority={t.priority} showIcon={false} />
                      </div>
                      <h4 className="text-xs font-medium text-text-primary line-clamp-2">{t.title}</h4>
                      <div className="flex items-center justify-between text-[10px] text-text-tertiary pt-2 border-t border-border/50">
                        <span>{t.assigned_agent_name || 'Unassigned'}</span>
                        <SLABadge targetDate={t.resolution_due_at} isBreached={t.is_overdue} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
