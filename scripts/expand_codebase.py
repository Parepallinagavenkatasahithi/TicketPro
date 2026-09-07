import os
import sys

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Generated: {path}")

def generate_frontend_ui_components():
    # 1. KanbanBoard.tsx
    write_file("frontend/src/components/ui/KanbanBoard.tsx", '''
import React from 'react';
import { Ticket, TicketStatusType } from '../../types';
import { TicketStatusBadge } from './TicketStatusBadge';
import { PriorityBadge } from './PriorityBadge';
import { Clock, User } from 'lucide-react';

interface KanbanColumn {
  id: TicketStatusType;
  title: string;
}

interface KanbanBoardProps {
  tickets: Ticket[];
  onTicketClick?: (ticket: Ticket) => void;
}

const COLUMNS: KanbanColumn[] = [
  { id: 'NEW', title: 'New Submissions' },
  { id: 'OPEN', title: 'Open Queue' },
  { id: 'IN_PROGRESS', title: 'In Progress' },
  { id: 'WAITING_FOR_USER', title: 'Waiting on User' },
  { id: 'RESOLVED', title: 'Resolved' }
];

export const KanbanBoard: React.FC<KanbanBoardProps> = ({ tickets, onTicketClick }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 overflow-x-auto pb-4">
      {COLUMNS.map((col) => {
        const colTickets = tickets.filter((t) => t.status === col.id);
        return (
          <div key={col.id} className="bg-slate-100 dark:bg-slate-900/60 rounded-xl p-3 flex flex-col min-h-[500px]">
            <div className="flex items-center justify-between mb-3 px-1">
              <h3 className="font-bold text-xs uppercase tracking-wider text-slate-700 dark:text-slate-300">
                {col.title}
              </h3>
              <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                {colTickets.length}
              </span>
            </div>

            <div className="space-y-2.5 flex-1 overflow-y-auto">
              {colTickets.map((ticket) => (
                <div
                  key={ticket.id}
                  onClick={() => onTicketClick && onTicketClick(ticket)}
                  className="bg-white dark:bg-slate-800 p-3.5 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700/80 hover:shadow-md transition-all cursor-pointer space-y-2"
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-mono font-bold text-indigo-600 dark:text-indigo-400">
                      {ticket.ticket_number}
                    </span>
                    <PriorityBadge priority={ticket.priority} />
                  </div>

                  <h4 className="font-semibold text-sm text-slate-900 dark:text-slate-100 line-clamp-2 leading-snug">
                    {ticket.title}
                  </h4>

                  <div className="pt-2 border-t border-slate-100 dark:border-slate-700/50 flex items-center justify-between text-xs text-slate-500">
                    <span className="flex items-center gap-1">
                      <User className="h-3 w-3" />
                      {ticket.assigned_agent_name || 'Unassigned'}
                    </span>
                    <span className="flex items-center gap-1 text-[11px]">
                      <Clock className="h-3 w-3" />
                      {new Date(ticket.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};
''')

    # 2. WorkflowStepper.tsx
    write_file("frontend/src/components/ui/WorkflowStepper.tsx", '''
import React from 'react';
import { CheckCircle2, Circle } from 'lucide-react';

export interface StepItem {
  id: string;
  label: string;
  description?: string;
}

interface WorkflowStepperProps {
  steps: StepItem[];
  currentStepIndex: number;
}

export const WorkflowStepper: React.FC<WorkflowStepperProps> = ({ steps, currentStepIndex }) => {
  return (
    <div className="w-full py-4">
      <div className="flex items-center justify-between relative">
        {steps.map((step, idx) => {
          const isCompleted = idx < currentStepIndex;
          const isCurrent = idx === currentStepIndex;

          return (
            <div key={step.id} className="flex-1 flex flex-col items-center relative z-10">
              <div
                className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs transition-colors ${
                  isCompleted
                    ? 'bg-emerald-600 text-white'
                    : isCurrent
                    ? 'bg-indigo-600 text-white ring-4 ring-indigo-100 dark:ring-indigo-950'
                    : 'bg-slate-200 dark:bg-slate-800 text-slate-500'
                }`}
              >
                {isCompleted ? <CheckCircle2 className="h-5 w-5" /> : idx + 1}
              </div>
              <span className={`mt-2 text-xs font-medium text-center ${isCurrent ? 'text-indigo-600 font-bold' : 'text-slate-600'}`}>
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
''')

    # 3. FilterBuilder.tsx
    write_file("frontend/src/components/ui/FilterBuilder.tsx", '''
import React, { useState } from 'react';
import { Filter, X, RefreshCw } from 'lucide-react';

export interface FilterCriterion {
  field: string;
  operator: 'equals' | 'contains' | 'in' | 'greater_than';
  value: string;
}

interface FilterBuilderProps {
  onApplyFilters: (filters: FilterCriterion[]) => void;
}

export const FilterBuilder: React.FC<FilterBuilderProps> = ({ onApplyFilters }) => {
  const [criteria, setCriteria] = useState<FilterCriterion[]>([
    { field: 'status', operator: 'equals', value: '' }
  ]);

  const addCriterion = () => {
    setCriteria([...criteria, { field: 'priority', operator: 'equals', value: '' }]);
  };

  const removeCriterion = (idx: number) => {
    setCriteria(criteria.filter((_, i) => i !== idx));
  };

  return (
    <div className="bg-slate-50 dark:bg-slate-900/80 p-4 rounded-xl border border-slate-200 dark:border-slate-800 space-y-3">
      <div className="flex items-center justify-between text-xs font-bold text-slate-700 dark:text-slate-300">
        <span className="flex items-center gap-1.5"><Filter className="h-4 w-4 text-indigo-600" /> Advanced Filter Criteria</span>
        <button onClick={addCriterion} className="text-indigo-600 hover:underline">+ Add Condition</button>
      </div>

      <div className="space-y-2">
        {criteria.map((item, idx) => (
          <div key={idx} className="flex items-center gap-2 text-xs">
            <select
              value={item.field}
              onChange={(e) => {
                const next = [...criteria];
                next[idx].field = e.target.value;
                setCriteria(next);
              }}
              className="p-2 rounded-lg border dark:bg-slate-800 dark:border-slate-700"
            >
              <option value="status">Status</option>
              <option value="priority">Priority</option>
              <option value="category">Category</option>
              <option value="department">Department</option>
            </select>

            <select
              value={item.operator}
              onChange={(e) => {
                const next = [...criteria];
                next[idx].operator = e.target.value as any;
                setCriteria(next);
              }}
              className="p-2 rounded-lg border dark:bg-slate-800 dark:border-slate-700"
            >
              <option value="equals">Equals</option>
              <option value="contains">Contains</option>
              <option value="in">In List</option>
            </select>

            <input
              type="text"
              placeholder="Value..."
              value={item.value}
              onChange={(e) => {
                const next = [...criteria];
                next[idx].value = e.target.value;
                setCriteria(next);
              }}
              className="flex-1 p-2 rounded-lg border dark:bg-slate-800 dark:border-slate-700"
            />

            <button onClick={() => removeCriterion(idx)} className="p-1 text-slate-400 hover:text-rose-600">
              <X className="h-4 w-4" />
            </button>
          </div>
        ))}
      </div>

      <div className="flex justify-end gap-2 pt-2">
        <button onClick={() => onApplyFilters(criteria)} className="px-3 py-1.5 rounded-lg bg-indigo-600 text-white font-medium text-xs">
          Apply Filters
        </button>
      </div>
    </div>
  );
};
''')

if __name__ == "__main__":
    generate_frontend_ui_components()
