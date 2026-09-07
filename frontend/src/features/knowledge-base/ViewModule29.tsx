import React, { useState } from 'react';
import { Search, Filter, RefreshCw, CheckCircle2, ChevronRight, BarChart2, Shield } from 'lucide-react';

export interface KnowledgeBaseItem29 {
  id: number;
  code: string;
  name: string;
  category: string;
  status: string;
  priority: string;
  created_at: string;
}

interface KnowledgeBaseViewModule29Props {
  title?: string;
  onItemSelect?: (item: KnowledgeBaseItem29) => void;
}

export const KnowledgeBaseViewModule29: React.FC<KnowledgeBaseViewModule29Props> = ({
  title = "Knowledge Base & Documentation Component 29",
  onItemSelect
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string>('ALL');

  const mockData: KnowledgeBaseItem29[] = [
    { id: 101, code: "KNO-29-001", name: "Knowledge Base & Documentation Record A", category: "ENTERPRISE", status: "ACTIVE", priority: "HIGH", created_at: "2026-09-01T10:00:00Z" },
    { id: 102, code: "KNO-29-002", name: "Knowledge Base & Documentation Record B", category: "STANDARD", status: "PENDING", priority: "MEDIUM", created_at: "2026-09-02T14:30:00Z" },
    { id: 103, code: "KNO-29-003", name: "Knowledge Base & Documentation Record C", category: "CRITICAL", status: "IN_REVIEW", priority: "CRITICAL", created_at: "2026-09-03T09:15:00Z" }
  ];

  const filteredItems = mockData.filter((item) => {
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) || item.code.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = selectedStatus === 'ALL' || item.status === selectedStatus;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Shield className="h-5 w-5 text-indigo-600" /> {title}
          </h3>
          <p className="text-xs text-slate-500">Enterprise operational view module for Knowledge Base & Documentation.</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300">
            v2.4.29
          </span>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search code, title, or category..."
            className="w-full pl-9 pr-4 py-2 text-xs bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:text-slate-200"
          />
        </div>
        <select
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
          className="py-2 px-3 text-xs bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg dark:text-slate-200"
        >
          <option value="ALL">All Statuses</option>
          <option value="ACTIVE">Active</option>
          <option value="PENDING">Pending</option>
          <option value="IN_REVIEW">In Review</option>
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="bg-slate-50 dark:bg-slate-800/80 text-slate-600 dark:text-slate-400 font-semibold">
              <th className="py-2.5 px-3">Code</th>
              <th className="py-2.5 px-3">Name</th>
              <th className="py-2.5 px-3">Category</th>
              <th className="py-2.5 px-3">Priority</th>
              <th className="py-2.5 px-3">Status</th>
              <th className="py-2.5 px-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {filteredItems.map((item) => (
              <tr key={item.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition-colors">
                <td className="py-2.5 px-3 font-mono font-semibold text-indigo-600 dark:text-indigo-400">{item.code}</td>
                <td className="py-2.5 px-3 font-medium text-slate-800 dark:text-slate-200">{item.name}</td>
                <td className="py-2.5 px-3 text-slate-500">{item.category}</td>
                <td className="py-2.5 px-3">
                  <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${item.priority === 'CRITICAL' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'}`}>
                    {item.priority}
                  </span>
                </td>
                <td className="py-2.5 px-3">
                  <span className="inline-flex items-center gap-1 font-semibold text-emerald-600">
                    <CheckCircle2 className="h-3 w-3" /> {item.status}
                  </span>
                </td>
                <td className="py-2.5 px-3 text-right">
                  <button
                    onClick={() => onItemSelect && onItemSelect(item)}
                    className="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-indigo-600"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
