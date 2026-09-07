import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { apiFetch } from '../../services/api';
import {
  DashboardMetrics, TicketTrendPoint, PriorityDistribution,
  Ticket, Announcement
} from '../../types';
import { StatCard } from '../../components/ui/StatCard';
import { TicketStatusBadge } from '../../components/ui/TicketStatusBadge';
import { PriorityBadge } from '../../components/ui/PriorityBadge';
import { SLABadge } from '../../components/ui/SLABadge';
import {
  Ticket as TicketIcon, Clock, CheckCircle2, AlertTriangle, AlertCircle,
  PlusCircle, Megaphone, ShieldAlert, ArrowRight, BookOpen, Layers
} from 'lucide-react';
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, Legend
} from 'recharts';
import { formatTimeAgo } from '../../lib/utils';

export const DashboardPage: React.FC = () => {
  const { user, hasPermission } = useAuth();
  const navigate = useNavigate();
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [trends, setTrends] = useState<TicketTrendPoint[]>([]);
  const [priorities, setPriorities] = useState<PriorityDistribution[]>([]);
  const [recentTickets, setRecentTickets] = useState<Ticket[]>([]);
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [timeRange, setTimeRange] = useState('7d');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        const [mRes, tRes, pRes, tkRes, aRes] = await Promise.all([
          apiFetch<DashboardMetrics>('/analytics/dashboard'),
          apiFetch<TicketTrendPoint[]>('/analytics/trends'),
          apiFetch<PriorityDistribution[]>('/analytics/priorities'),
          apiFetch<Ticket[]>('/tickets?limit=8'),
          apiFetch<Announcement[]>('/announcements?limit=3'),
        ]);

        setMetrics(mRes);
        setTrends(tRes || []);
        setPriorities(pRes || []);
        setRecentTickets(tkRes || []);
        setAnnouncements(aRes || []);
      } catch (err) {
        console.error('Error loading dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [timeRange]);

  const COLORS = {
    HIGH: '#E44D5E',
    CRITICAL: '#B32C3B',
    MEDIUM: '#E6A23C',
    LOW: '#2E9B62',
  };

  return (
    <div className="space-y-6">
      {/* Page Header (Section 9) */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-text-primary tracking-tight">
            Good morning, {user?.full_name?.split(' ')[0] || 'User'}!
          </h1>
          <p className="text-xs text-text-secondary mt-0.5">
            Here's an overview of your support operations and service metrics
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-2 bg-surface border border-border rounded-xl text-xs font-semibold text-text-secondary focus:outline-none shadow-sm"
          >
            <option value="7d">This Week</option>
            <option value="30d">This Month</option>
            <option value="90d">Last 30 Days</option>
          </select>
          <button
            onClick={() => {
              const searchBtn = document.getElementById('global-search-trigger');
              if (searchBtn) searchBtn.click();
            }}
            className="flex items-center space-x-2 px-4 py-2 bg-brand text-white text-xs font-semibold rounded-xl shadow-sm hover:bg-brand-600 transition-colors"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Create Ticket</span>
          </button>
        </div>
      </div>

      {/* KPI Cards Grid (Section 10) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Total Tickets"
          value={metrics?.total_tickets ?? 0}
          icon={TicketIcon}
          trendPercentage={metrics?.total_trend_percentage}
          iconColor="text-brand-500"
          bgColor="bg-brand-50"
          onClick={() => navigate('/tickets')}
        />
        <StatCard
          title="Open Tickets"
          value={metrics?.open_tickets ?? 0}
          icon={Clock}
          trendPercentage={metrics?.open_trend_percentage}
          iconColor="text-brand-600"
          bgColor="bg-purple-100"
          onClick={() => navigate('/tickets?status=OPEN')}
        />
        <StatCard
          title="In Progress"
          value={metrics?.in_progress_tickets ?? 0}
          icon={Layers}
          trendPercentage={metrics?.in_progress_trend_percentage}
          iconColor="text-info-dark"
          bgColor="bg-info-light"
          onClick={() => navigate('/tickets?status=IN_PROGRESS')}
        />
        <StatCard
          title="Resolved"
          value={metrics?.resolved_tickets ?? 0}
          icon={CheckCircle2}
          trendPercentage={metrics?.resolved_trend_percentage}
          iconColor="text-success-dark"
          bgColor="bg-success-light"
          onClick={() => navigate('/tickets?status=RESOLVED')}
        />
        <StatCard
          title="Overdue"
          value={metrics?.overdue_tickets ?? 0}
          icon={AlertTriangle}
          trendPercentage={metrics?.overdue_trend_percentage}
          iconColor="text-danger-dark"
          bgColor="bg-danger-light"
          onClick={() => navigate('/tickets?is_overdue=true')}
        />
      </div>

      {/* Charts Grid (Section 11 & 12) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Ticket Trends Chart (2 cols) */}
        <div className="lg:col-span-2 bg-surface p-5 rounded-2xl border border-border shadow-card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-text-primary">Ticket Volume Trends</h3>
              <p className="text-xs text-text-tertiary">Daily support ticket activity breakdown</p>
            </div>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorOpen" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#5B35D5" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#5B35D5" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorInp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4A78E8" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#4A78E8" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorRes" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2E9B62" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#2E9B62" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" stroke="#9398AA" fontSize={11} tickLine={false} />
                <YAxis stroke="#9398AA" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderRadius: '12px', border: '1px solid #E7E8EF', fontSize: '12px' }} />
                <Area type="monotone" dataKey="open" stroke="#5B35D5" fillOpacity={1} fill="url(#colorOpen)" name="Open" />
                <Area type="monotone" dataKey="in_progress" stroke="#4A78E8" fillOpacity={1} fill="url(#colorInp)" name="In Progress" />
                <Area type="monotone" dataKey="resolved" stroke="#2E9B62" fillOpacity={1} fill="url(#colorRes)" name="Resolved" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Priority Distribution Chart (1 col) */}
        <div className="bg-surface p-5 rounded-2xl border border-border shadow-card flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-text-primary">Tickets by Priority</h3>
            <p className="text-xs text-text-tertiary">Priority distribution of active ticket queue</p>
            <div className="h-52 w-full mt-2">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={priorities}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={80}
                    paddingAngle={3}
                    dataKey="count"
                    nameKey="priority"
                  >
                    {priorities.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[entry.priority as keyof typeof COLORS] || '#5B35D5'} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderRadius: '8px', fontSize: '12px' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-2 text-center pt-3 border-t border-border">
            {priorities.slice(0, 3).map((p) => (
              <div key={p.priority}>
                <span className="text-[10px] uppercase font-bold text-text-tertiary">{p.priority}</span>
                <p className="text-sm font-bold text-text-primary">{p.count}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Middle Row: Operational Alert + Announcements + SLA Widget (Section 13, 14, 17) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Operational Alert Card (Section 13) */}
        <div className="bg-gradient-to-br from-red-50 to-orange-50 p-5 rounded-2xl border border-red-200 shadow-card flex flex-col justify-between">
          <div className="flex items-start space-x-3">
            <div className="p-2.5 rounded-xl bg-danger text-white shadow-sm flex-shrink-0">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-danger-dark">Improve Response Time</h4>
              <p className="text-xs text-text-secondary mt-1">
                You currently have <strong className="text-danger">{metrics?.overdue_tickets || 0} overdue tickets</strong> requiring immediate agent intervention.
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/tickets?is_overdue=true')}
            className="mt-4 w-full py-2.5 px-4 rounded-xl bg-danger text-white text-xs font-semibold hover:bg-danger-dark transition-colors shadow-sm text-center"
          >
            View Overdue Tickets
          </button>
        </div>

        {/* SLA Compliance Widget (Section 17) */}
        <div className="bg-surface p-5 rounded-2xl border border-border shadow-card flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-text-tertiary">SLA Compliance Rate</span>
              <span className="text-xs font-bold text-success-dark bg-success-light px-2 py-0.5 rounded-full">
                Target 90%+
              </span>
            </div>
            <div className="flex items-baseline space-x-2 mt-2">
              <span className="text-3xl font-extrabold text-brand-600">{metrics?.sla_compliance_rate || 94.5}%</span>
              <span className="text-xs text-text-tertiary">({metrics?.sla_compliant_tickets || 0} of {metrics?.sla_total_eligible || 0} tickets)</span>
            </div>
            <div className="w-full bg-border rounded-full h-2 mt-3 overflow-hidden">
              <div className="bg-success h-full rounded-full" style={{ width: `${metrics?.sla_compliance_rate || 94.5}%` }} />
            </div>
          </div>
          <button
            onClick={() => navigate('/sla')}
            className="mt-4 text-xs font-semibold text-brand-600 hover:underline flex items-center justify-end"
          >
            View SLA Compliance Report <ArrowRight className="w-3.5 h-3.5 ml-1" />
          </button>
        </div>

        {/* Recent Announcements Widget (Section 14) */}
        <div className="bg-surface p-5 rounded-2xl border border-border shadow-card flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-text-tertiary flex items-center">
                <Megaphone className="w-4 h-4 mr-1.5 text-brand-500" /> Announcements
              </h4>
              <button onClick={() => navigate('/announcements')} className="text-xs text-brand-600 font-semibold hover:underline">
                View All
              </button>
            </div>
            <div className="space-y-2">
              {announcements.slice(0, 2).map((a) => (
                <div key={a.id} className="p-2.5 rounded-xl bg-surface-subtle border border-border/60 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-text-primary truncate">{a.title}</span>
                    <span className="text-[10px] text-text-tertiary">{formatTimeAgo(a.created_at)}</span>
                  </div>
                  <p className="text-text-secondary mt-1 line-clamp-1">{a.content}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Tickets Table (Section 15) */}
      <div className="bg-surface rounded-2xl border border-border shadow-card overflow-hidden">
        <div className="p-5 border-b border-border flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-text-primary">Recent Tickets</h3>
            <p className="text-xs text-text-tertiary">Real-time enterprise support ticket stream</p>
          </div>
          <button
            onClick={() => navigate('/tickets')}
            className="text-xs font-semibold text-brand-600 hover:underline flex items-center"
          >
            View All Tickets <ArrowRight className="w-3.5 h-3.5 ml-1" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-surface-subtle border-b border-border text-text-tertiary font-semibold uppercase tracking-wider">
              <tr>
                <th className="px-5 py-3.5">Ticket ID</th>
                <th className="px-5 py-3.5">Subject</th>
                <th className="px-5 py-3.5">Requester</th>
                <th className="px-5 py-3.5">Priority</th>
                <th className="px-5 py-3.5">Status</th>
                <th className="px-5 py-3.5">Assigned Agent</th>
                <th className="px-5 py-3.5">SLA Countdown</th>
                <th className="px-5 py-3.5">Updated</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-text-primary">
              {recentTickets.map((t) => (
                <tr
                  key={t.id}
                  onClick={() => navigate(`/tickets/${t.id}`)}
                  className="hover:bg-surface-subtle/80 cursor-pointer transition-colors"
                >
                  <td className="px-5 py-3.5 font-bold text-brand-600">{t.ticket_number}</td>
                  <td className="px-5 py-3.5 font-medium max-w-xs truncate">{t.title}</td>
                  <td className="px-5 py-3.5">{t.requester_name || 'Employee'}</td>
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
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
