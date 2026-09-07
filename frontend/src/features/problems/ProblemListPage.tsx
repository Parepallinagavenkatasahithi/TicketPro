import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { Problem } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { AlertOctagon, Plus, Search, FileText } from 'lucide-react';

export function ProblemListPage() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProblems();
  }, []);

  const loadProblems = async () => {
    setLoading(true);
    try {
      const data = await api.getProblems();
      setProblems(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const columns: Column<Problem>[] = [
    { key: 'problem_number', header: 'PRB Number', render: (p) => <span className="font-semibold text-rose-600 dark:text-rose-400">{p.problem_number}</span> },
    { key: 'title', header: 'Problem Overview' },
    { key: 'impact', header: 'Impact', render: (p) => <span className="px-2 py-0.5 rounded text-xs font-bold bg-rose-100 text-rose-800">{p.impact}</span> },
    { key: 'status', header: 'Status', render: (p) => <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800">{p.status}</span> },
    { key: 'owner_name', header: 'Problem Owner' }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <AlertOctagon className="h-6 w-6 text-rose-600" /> ITIL Problem Management
        </h1>
        <p className="text-sm text-slate-500">Investigate root causes, record workarounds, and minimize recurring incidents.</p>
      </div>
      {loading ? <div className="py-12 text-center text-slate-400">Loading problem tickets...</div> : <DataTable columns={columns} data={problems} />}
    </div>
  );
}
