import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { Asset } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { HardDrive, Plus, CheckCircle2, AlertTriangle, XCircle, Wrench } from 'lucide-react';

export function AssetListPage() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [form, setForm] = useState({
    asset_tag: '',
    name: '',
    category: 'HARDWARE',
    model_number: '',
    serial_number: '',
    status: 'IN_USE',
    location: '',
    purchase_cost: 0,
    vendor_name: ''
  });

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    setLoading(true);
    try {
      const data = await api.getAssets();
      setAssets(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createAsset(form);
      setShowCreateModal(false);
      setForm({
        asset_tag: '',
        name: '',
        category: 'HARDWARE',
        model_number: '',
        serial_number: '',
        status: 'IN_USE',
        location: '',
        purchase_cost: 0,
        vendor_name: ''
      });
      loadAssets();
    } catch (err: any) {
      alert(err.message || 'Failed to create asset');
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'IN_USE':
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300"><CheckCircle2 className="w-3 h-3" /> In Use</span>;
      case 'IN_STOCK':
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 dark:bg-blue-950/60 dark:text-blue-300">In Stock</span>;
      case 'UNDER_REPAIR':
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300"><Wrench className="w-3 h-3" /> Repair</span>;
      default:
        return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300">{status}</span>;
    }
  };

  const columns: Column<Asset>[] = [
    { key: 'asset_tag', header: 'Asset Tag', render: (a) => <span className="font-semibold text-indigo-600 dark:text-indigo-400">{a.asset_tag}</span> },
    { key: 'name', header: 'Device Name' },
    { key: 'category', header: 'Category' },
    { key: 'model_number', header: 'Model / Serial', render: (a) => <span className="text-xs text-slate-500">{a.model_number || 'N/A'} ({a.serial_number || 'N/A'})</span> },
    { key: 'status', header: 'Status', render: (a) => getStatusBadge(a.status) },
    { key: 'location', header: 'Location', render: (a) => a.location || 'HQ Main' },
    { key: 'purchase_cost', header: 'Cost', render: (a) => a.purchase_cost ? `$${a.purchase_cost.toLocaleString()}` : '—' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <HardDrive className="h-6 w-6 text-indigo-600" /> IT Asset Management (CMDB)
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Track company hardware, software licenses, lifecycle status, and cost allocation.</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm px-4 py-2.5 rounded-xl shadow-sm transition-colors"
        >
          <Plus className="h-4 w-4" /> Register Asset
        </button>
      </div>

      {loading ? (
        <div className="py-12 text-center text-slate-400">Loading IT assets...</div>
      ) : (
        <DataTable columns={columns} data={assets} searchPlaceholder="Search asset tag, serial number, model..." />
      )}

      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 rounded-2xl max-w-lg w-full p-6 shadow-xl border border-slate-200 dark:border-slate-800">
            <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4">Register New IT Asset</h2>
            <form onSubmit={handleCreate} className="space-y-4 text-sm">
              <div>
                <label className="block font-medium text-slate-700 dark:text-slate-300 mb-1">Asset Tag</label>
                <input
                  type="text"
                  required
                  placeholder="AST-2026-001"
                  value={form.asset_tag}
                  onChange={(e) => setForm({ ...form, asset_tag: e.target.value })}
                  className="w-full p-2.5 border rounded-lg dark:bg-slate-800 dark:border-slate-700 dark:text-slate-100"
                />
              </div>
              <div>
                <label className="block font-medium text-slate-700 dark:text-slate-300 mb-1">Device Name</label>
                <input
                  type="text"
                  required
                  placeholder="Dell XPS 15 Developer Workstation"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="w-full p-2.5 border rounded-lg dark:bg-slate-800 dark:border-slate-700 dark:text-slate-100"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-medium text-slate-700 dark:text-slate-300 mb-1">Category</label>
                  <select
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                    className="w-full p-2.5 border rounded-lg dark:bg-slate-800 dark:border-slate-700 dark:text-slate-100"
                  >
                    <option value="HARDWARE">HARDWARE</option>
                    <option value="SOFTWARE">SOFTWARE</option>
                    <option value="NETWORK">NETWORK</option>
                    <option value="PERIPHERAL">PERIPHERAL</option>
                  </select>
                </div>
                <div>
                  <label className="block font-medium text-slate-700 dark:text-slate-300 mb-1">Purchase Cost ($)</label>
                  <input
                    type="number"
                    value={form.purchase_cost}
                    onChange={(e) => setForm({ ...form, purchase_cost: Number(e.target.value) })}
                    className="w-full p-2.5 border rounded-lg dark:bg-slate-800 dark:border-slate-700 dark:text-slate-100"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700"
                >
                  Save Asset
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
