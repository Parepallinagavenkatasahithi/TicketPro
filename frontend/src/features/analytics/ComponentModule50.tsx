import React, { useState } from 'react';
import { Search, Filter, RefreshCw, CheckCircle2, ChevronRight, BarChart2, Shield, Settings, Clock, User, AlertCircle } from 'lucide-react';

export interface AnalyticsDashboardItemData50 {
  id: number;
  item_code: string;
  item_title: string;
  category_type: string;
  current_status: string;
  priority_level: string;
  assigned_to: string;
  created_date: string;
  score_value: number;
}

interface AnalyticsDashboardComponentModule50Props {
  headerTitle?: string;
  onSelectRecord?: (record: AnalyticsDashboardItemData50) => void;
  refreshInterval?: number;
}

export const AnalyticsDashboardComponentModule50: React.FC<AnalyticsDashboardComponentModule50Props> = ({
  headerTitle = "Recharts Analytics & KPI Dashboards Module 50",
  onSelectRecord,
  refreshInterval = 30
}) => {
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [filterCategory, setFilterCategory] = useState<string>('ALL');
  const [activeTab, setActiveTab] = useState<'GRID' | 'ANALYTICS' | 'SETTINGS'>('GRID');

  const dataset: AnalyticsDashboardItemData50[] = [
    { id: 201, item_code: "ANAL-50-01", item_title: "Recharts Analytics & KPI Dashboards Record A", category_type: "ENTERPRISE", current_status: "ACTIVE", priority_level: "HIGH", assigned_to: "Alex Rivera", created_date: "2026-09-01T10:00:00Z", score_value: 98.5 },
    { id: 202, item_code: "ANAL-50-02", item_title: "Recharts Analytics & KPI Dashboards Record B", category_type: "STANDARD", current_status: "PENDING", priority_level: "MEDIUM", assigned_to: "David Kim", created_date: "2026-09-02T14:30:00Z", score_value: 84.2 },
    { id: 203, item_code: "ANAL-50-03", item_title: "Recharts Analytics & KPI Dashboards Record C", category_type: "CRITICAL", current_status: "IN_REVIEW", priority_level: "CRITICAL", assigned_to: "Rachel Chen", created_date: "2026-09-03T09:15:00Z", score_value: 92.0 }
  ];

  const filteredDataset = dataset.filter((row) => {
    const matchQuery = row.item_title.toLowerCase().includes(searchTerm.toLowerCase()) || row.item_code.toLowerCase().includes(searchTerm.toLowerCase());
    const matchCat = filterCategory === 'ALL' || row.category_type === filterCategory;
    return matchQuery && matchCat;
  });

  return (
    <div className="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Shield className="h-5 w-5 text-indigo-600" /> {headerTitle}
          </h3>
          <p className="text-xs text-slate-500">Production ITSM operational view component for Recharts Analytics & KPI Dashboards.</p>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-lg text-xs font-semibold">
            <button
              onClick={() => setActiveTab('GRID')}
              className={`px-3 py-1 rounded-md transition-colors ${activeTab === 'GRID' ? 'bg-white dark:bg-slate-700 text-indigo-600 shadow-xs' : 'text-slate-500'}`}
            >
              Data Grid
            </button>
            <button
              onClick={() => setActiveTab('ANALYTICS')}
              className={`px-3 py-1 rounded-md transition-colors ${activeTab === 'ANALYTICS' ? 'bg-white dark:bg-slate-700 text-indigo-600 shadow-xs' : 'text-slate-500'}`}
            >
              Analytics
            </button>
          </div>
          <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300">
            v3.5.50
          </span>
        </div>
      </div>

      {activeTab === 'GRID' && (
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row items-center gap-3">
            <div className="relative flex-1 w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search record code, title, or assignee..."
                className="w-full pl-9 pr-4 py-2 text-xs bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:text-slate-200"
              />
            </div>
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="py-2 px-3 text-xs bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg dark:text-slate-200"
            >
              <option value="ALL">All Categories</option>
              <option value="ENTERPRISE">Enterprise</option>
              <option value="STANDARD">Standard</option>
              <option value="CRITICAL">Critical</option>
            </select>
          </div>

          <div className="overflow-x-auto border border-slate-100 dark:border-slate-800 rounded-lg">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="bg-slate-50 dark:bg-slate-800/80 text-slate-600 dark:text-slate-400 font-semibold border-b border-slate-100 dark:border-slate-800">
                  <th className="py-2.5 px-3">Item Code</th>
                  <th className="py-2.5 px-3">Title</th>
                  <th className="py-2.5 px-3">Category</th>
                  <th className="py-2.5 px-3">Priority</th>
                  <th className="py-2.5 px-3">Assigned To</th>
                  <th className="py-2.5 px-3">Score</th>
                  <th className="py-2.5 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {filteredDataset.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition-colors">
                    <td className="py-2.5 px-3 font-mono font-semibold text-indigo-600 dark:text-indigo-400">{row.item_code}</td>
                    <td className="py-2.5 px-3 font-medium text-slate-800 dark:text-slate-200">{row.item_title}</td>
                    <td className="py-2.5 px-3 text-slate-500">{row.category_type}</td>
                    <td className="py-2.5 px-3">
                      <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${row.priority_level === 'CRITICAL' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'}`}>
                        {row.priority_level}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-slate-600 dark:text-slate-400">{row.assigned_to}</td>
                    <td className="py-2.5 px-3 font-bold text-slate-700 dark:text-slate-300">{row.score_value}%</td>
                    <td className="py-2.5 px-3 text-right">
                      <button
                        onClick={() => onSelectRecord && onSelectRecord(row)}
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
      )}

      {activeTab === 'ANALYTICS' && (
        <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl space-y-3">
          <h4 className="font-bold text-xs text-slate-700 dark:text-slate-300 flex items-center gap-2">
            <BarChart2 className="h-4 w-4 text-indigo-600" /> Module Performance Analytics
          </h4>
          <div className="grid grid-cols-3 gap-3 text-xs">
            <div className="p-3 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
              <span className="text-slate-500 block">Total Records</span>
              <span className="text-lg font-bold text-slate-900 dark:text-slate-100">{dataset.length}</span>
            </div>
            <div className="p-3 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
              <span className="text-slate-500 block">Avg KPI Score</span>
              <span className="text-lg font-bold text-emerald-600">91.5%</span>
            </div>
            <div className="p-3 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
              <span className="text-slate-500 block">Refresh Frequency</span>
              <span className="text-lg font-bold text-indigo-600">{refreshInterval}s</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
