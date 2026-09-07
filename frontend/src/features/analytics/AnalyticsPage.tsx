import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { DashboardMetrics, TicketTrendPoint } from '../../types';
import { BarChart3, Download, TrendingUp, Clock, CheckCircle, Users } from 'lucide-react';
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, BarChart, Bar
} from 'recharts';

export const AnalyticsPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [trends, setTrends] = useState<TicketTrendPoint[]>([]);

  useEffect(() => {
    Promise.all([
      apiFetch<DashboardMetrics>('/analytics/dashboard'),
      apiFetch<TicketTrendPoint[]>('/analytics/trends'),
    ])
      .then(([m, t]) => {
        setMetrics(m);
        setTrends(t || []);
      })
      .catch(console.error);
  }, []);

  const handleExportCSV = async () => {
    try {
      const csvText = await apiFetch<string>('/reports/export/csv');
      const blob = new Blob([csvText], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'ticketpro_operations_report.csv';
      a.click();
    } catch (err) {
      console.error('Export failed:', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary tracking-tight">Reports & Operations Analytics</h1>
          <p className="text-xs text-text-secondary mt-0.5">
            Deep insights into ticket volume, agent productivity, and SLA compliance
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          className="flex items-center space-x-2 px-4 py-2 bg-brand text-white text-xs font-semibold rounded-xl shadow-sm hover:bg-brand-600 transition-colors"
        >
          <Download className="w-4 h-4" />
          <span>Export CSV Report</span>
        </button>
      </div>

      <div className="bg-surface p-6 rounded-2xl border border-border shadow-card space-y-4">
        <h3 className="text-sm font-bold text-text-primary">Weekly Ticket Resolution Trend</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={trends}>
              <XAxis dataKey="date" stroke="#9398AA" fontSize={12} tickLine={false} />
              <YAxis stroke="#9398AA" fontSize={12} tickLine={false} />
              <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderRadius: '12px', fontSize: '12px' }} />
              <Bar dataKey="open" fill="#5B35D5" name="Open" radius={[4, 4, 0, 0]} />
              <Bar dataKey="in_progress" fill="#4A78E8" name="In Progress" radius={[4, 4, 0, 0]} />
              <Bar dataKey="resolved" fill="#2E9B62" name="Resolved" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
