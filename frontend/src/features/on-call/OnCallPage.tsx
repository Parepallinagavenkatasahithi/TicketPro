import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { OnCallRotation } from '../../types';
import { Shield, Clock, UserCheck, Calendar } from 'lucide-react';

export function OnCallPage() {
  const [rotations, setRotations] = useState<OnCallRotation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRotations();
  }, []);

  const loadRotations = async () => {
    setLoading(true);
    try {
      const data = await api.getOnCallRotations();
      setRotations(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Shield className="h-6 w-6 text-emerald-600" /> On-Call Rotations & Roster
        </h1>
        <p className="text-sm text-slate-500">24/7 Incident escalation rotas and automated active responder schedules.</p>
      </div>

      {loading ? (
        <div className="py-12 text-center text-slate-400">Loading on-call rosters...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {rotations.map((r) => (
            <div key={r.id} className="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-bold text-slate-800 dark:text-slate-200 text-base">{r.name}</h3>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">ACTIVE</span>
              </div>
              <p className="text-xs text-slate-500 mb-4">Department: {r.department_name || 'IT Infrastructure'} • Rota: {r.rotation_type}</p>
              
              <div className="space-y-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Current & Upcoming Shifts</h4>
                {r.shifts.length === 0 ? (
                  <p className="text-xs italic text-slate-400">No shifts scheduled for this week.</p>
                ) : (
                  r.shifts.map((s) => (
                    <div key={s.id} className="flex items-center justify-between p-2.5 bg-slate-50 dark:bg-slate-800/50 rounded-lg text-xs">
                      <div className="flex items-center gap-2">
                        <UserCheck className="h-4 w-4 text-emerald-600" />
                        <span className="font-semibold text-slate-800 dark:text-slate-200">{s.primary_user_name || 'Primary Engineer'}</span>
                      </div>
                      <span className="text-slate-500">{new Date(s.start_at).toLocaleDateString()} - {new Date(s.end_at).toLocaleDateString()}</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
