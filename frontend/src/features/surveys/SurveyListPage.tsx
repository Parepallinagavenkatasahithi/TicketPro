import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { SurveyResponse } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { Star, MessageSquare } from 'lucide-react';

export function SurveyListPage() {
  const [surveys, setSurveys] = useState<SurveyResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSurveys();
  }, []);

  const loadSurveys = async () => {
    setLoading(true);
    try {
      const data = await api.getSurveys();
      setSurveys(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const columns: Column<SurveyResponse>[] = [
    { key: 'ticket_number', header: 'Ticket Number', render: (s) => <span className="font-semibold text-indigo-600">{s.ticket_number}</span> },
    { key: 'respondent_name', header: 'Employee' },
    {
      key: 'rating',
      header: 'CSAT Rating',
      render: (s) => (
        <div className="flex items-center gap-1">
          {[...Array(5)].map((_, i) => (
            <Star key={i} className={`h-4 w-4 ${i < s.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200'}`} />
          ))}
          <span className="ml-1 text-xs font-bold text-slate-700">{s.rating}/5</span>
        </div>
      )
    },
    { key: 'feedback_text', header: 'Feedback Comments', render: (s) => <span className="text-xs italic text-slate-600">"{s.feedback_text || 'No comment provided.'}"</span> },
    { key: 'agent_name', header: 'Assigned Agent' }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Star className="h-6 w-6 text-amber-500 fill-amber-500" /> CSAT & Service Quality Ratings
        </h1>
        <p className="text-sm text-slate-500">Monitor employee satisfaction ratings and support service feedback.</p>
      </div>
      {loading ? <div className="py-12 text-center text-slate-400">Loading CSAT survey responses...</div> : <DataTable columns={columns} data={surveys} />}
    </div>
  );
}
