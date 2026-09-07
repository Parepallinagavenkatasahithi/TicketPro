import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { SLAPolicy } from '../../types';
import { Clock, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { PriorityBadge } from '../../components/ui/PriorityBadge';

export const SLAManagementPage: React.FC = () => {
  const [policies, setPolicies] = useState<SLAPolicy[]>([]);

  useEffect(() => {
    apiFetch<SLAPolicy[]>('/sla/policies')
      .then((data) => setPolicies(data || []))
      .catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary tracking-tight">SLA Management & Service Level Agreements</h1>
        <p className="text-xs text-text-secondary mt-0.5">
          Configure response and resolution time targets based on ticket priority levels
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {policies.map((p) => (
          <div key={p.id} className="bg-surface p-5 rounded-2xl border border-border shadow-card space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-text-primary">{p.name}</h3>
              <PriorityBadge priority={p.priority} />
            </div>

            <div className="space-y-2 text-xs border-t border-border pt-3">
              <div className="flex justify-between py-1 border-b border-border/50">
                <span className="text-text-tertiary">First Response Target:</span>
                <span className="font-bold text-brand-600">{p.max_first_response_minutes} mins</span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/50">
                <span className="text-text-tertiary">Resolution Target:</span>
                <span className="font-bold text-brand-600">{Math.round(p.max_resolution_minutes / 60)} hours</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-text-tertiary">Warning Threshold:</span>
                <span className="font-semibold text-warning-dark">{p.warning_threshold_percent}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
