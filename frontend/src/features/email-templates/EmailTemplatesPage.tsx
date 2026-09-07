import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { EmailTemplate } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { Mail, Plus, Code } from 'lucide-react';

export function EmailTemplatesPage() {
  const [templates, setTemplates] = useState<EmailTemplate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    setLoading(true);
    try {
      const data = await api.getEmailTemplates();
      setTemplates(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const columns: Column<EmailTemplate>[] = [
    { key: 'name', header: 'Template Name', render: (t) => <span className="font-semibold text-indigo-600">{t.name}</span> },
    { key: 'event_trigger', header: 'Event Trigger', render: (t) => <span className="px-2 py-0.5 rounded text-xs font-mono bg-purple-100 text-purple-800">{t.event_trigger}</span> },
    { key: 'subject_template', header: 'Email Subject' },
    { key: 'is_active', header: 'Active', render: (t) => t.is_active ? <span className="text-emerald-600 font-bold">ACTIVE</span> : <span className="text-slate-400">DISABLED</span> }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Mail className="h-6 w-6 text-indigo-600" /> Email Notification Templates
        </h1>
        <p className="text-sm text-slate-500">Customize automated notification emails for ticket events, SLA breaches, and approvals.</p>
      </div>
      {loading ? <div className="py-12 text-center text-slate-400">Loading notification templates...</div> : <DataTable columns={columns} data={templates} />}
    </div>
  );
}
