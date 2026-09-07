import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { TimeEntry } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { Clock, Plus, DollarSign } from 'lucide-react';

export function TimeTrackingPage() {
  const [entries, setEntries] = useState<TimeEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // For general list, fetch sample time entries
    loadEntries();
  }, []);

  const loadEntries = async () => {
    setLoading(true);
    try {
      // sample ticket ID 1 or fetch entries
      const data = await api.getTimeEntries(1);
      setEntries(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const columns: Column<TimeEntry>[] = [
    { key: 'ticket_number', header: 'Ticket Number', render: (t) => <span className="font-semibold text-indigo-600">{t.ticket_number}</span> },
    { key: 'user_name', header: 'Support Agent' },
    { key: 'activity_type', header: 'Activity Type' },
    { key: 'hours_spent', header: 'Hours Spent', render: (t) => <span className="font-bold text-slate-800">{t.hours_spent} hrs</span> },
    { key: 'description', header: 'Work Details' }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Clock className="h-6 w-6 text-indigo-600" /> Time Tracking & Effort Billing
        </h1>
        <p className="text-sm text-slate-500">Track hours spent by support engineers across incident resolution activities.</p>
      </div>
      {loading ? <div className="py-12 text-center text-slate-400">Loading logged time entries...</div> : <DataTable columns={columns} data={entries} />}
    </div>
  );
}
