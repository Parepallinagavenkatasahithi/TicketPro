import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { ApprovalRequest } from '../../types';
import { CheckSquare, Check, X, Clock } from 'lucide-react';
import { formatDate } from '../../lib/utils';

export const ApprovalListPage: React.FC = () => {
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);

  const fetchApprovals = async () => {
    try {
      const data = await apiFetch<ApprovalRequest[]>('/approvals');
      setApprovals(data || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchApprovals();
  }, []);

  const handleDecide = async (stepId: number, decision: 'APPROVED' | 'REJECTED') => {
    try {
      await apiFetch(`/approvals/steps/${stepId}/decide`, {
        method: 'PUT',
        body: JSON.stringify({ decision, notes: `Decision: ${decision}` }),
      });
      fetchApprovals();
    } catch (err: any) {
      alert(err.message || 'Decision failed');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary tracking-tight">Multi-step Approval Workflows</h1>
        <p className="text-xs text-text-secondary mt-0.5">
          Review pending privilege, software, and security authorization requests
        </p>
      </div>

      <div className="space-y-4">
        {approvals.length === 0 ? (
          <div className="bg-surface p-12 rounded-2xl border border-border text-center text-xs text-text-tertiary">
            No approval requests found in your inbox.
          </div>
        ) : (
          approvals.map((req) => (
            <div key={req.id} className="bg-surface p-5 rounded-2xl border border-border shadow-card space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-brand-600 mr-2">{req.ticket_number}</span>
                  <span className="text-sm font-bold text-text-primary">{req.title}</span>
                </div>
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                  req.status === 'APPROVED' ? 'bg-success-light text-success-dark' :
                  req.status === 'REJECTED' ? 'bg-danger-light text-danger-dark' :
                  'bg-warning-light text-warning-dark'
                }`}>
                  {req.status}
                </span>
              </div>

              <p className="text-xs text-text-secondary">{req.rationale || 'No rationale provided'}</p>

              <div className="pt-3 border-t border-border space-y-2">
                <div className="text-[11px] font-bold uppercase tracking-wider text-text-tertiary">Approval Steps</div>
                {req.steps.map((step) => (
                  <div key={step.id} className="flex items-center justify-between p-2.5 rounded-xl bg-surface-subtle border border-border/60 text-xs">
                    <div>
                      <span className="font-bold text-text-primary">Step {step.step_number}: {step.approver_name}</span>
                      {step.decision_notes && <span className="text-text-tertiary ml-2">({step.decision_notes})</span>}
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        step.status === 'APPROVED' ? 'bg-success-light text-success-dark' :
                        step.status === 'REJECTED' ? 'bg-danger-light text-danger-dark' :
                        'bg-warning-light text-warning-dark'
                      }`}>
                        {step.status}
                      </span>
                      {step.status === 'PENDING' && (
                        <div className="flex space-x-1">
                          <button
                            onClick={() => handleDecide(step.id, 'APPROVED')}
                            className="p-1 rounded bg-success text-white hover:bg-success-dark"
                          >
                            <Check className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => handleDecide(step.id, 'REJECTED')}
                            className="p-1 rounded bg-danger text-white hover:bg-danger-dark"
                          >
                            <X className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
