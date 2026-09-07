import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { ChangeRequest } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { GitPullRequest, Plus, Clock, ShieldAlert, CheckCircle2 } from 'lucide-react';

export function ChangeRequestListPage() {
  const [changes, setChanges] = useState<ChangeRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChanges();
  }, []);

  const loadChanges = async () => {
    setLoading(true);
    try {
      const data = await api.getChangeRequests();
      setChanges(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const columns: Column<ChangeRequest>[] = [
    { key: 'change_number', header: 'CHG Number', render: (c) => <span className="font-semibold text-purple-600 dark:text-purple-400">{c.change_number}</span> },
    { key: 'title', header: 'Change Title' },
    { key: 'category', header: 'Category' },
    {
      key: 'risk_level',
      header: 'Risk Level',
      render: (c) => (
        <span className={`px-2 py-0.5 rounded text-xs font-bold ${
          c.risk_level === 'CRITICAL' ? 'bg-red-100 text-red-800' :
          c.risk_level === 'HIGH' ? 'bg-orange-100 text-orange-800' : 'bg-blue-100 text-blue-800'
        }`}>
          {c.risk_level}
        </span>
      )
    },
    { key: 'status', header: 'Status', render: (c) => <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-100 text-purple-800">{c.status}</span> },
    { key: 'requester_name', header: 'Requester' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <GitPullRequest className="h-6 w-6 text-purple-600" /> ITIL Change Management (CAB)
          </h1>
          <p className="text-sm text-slate-500">Plan, review, and authorize system deployments and infrastructure changes.</p>
        </div>
      </div>
      {loading ? <div className="py-12 text-center text-slate-400">Loading change requests...</div> : <DataTable columns={columns} data={changes} />}
    </div>
  );
}
