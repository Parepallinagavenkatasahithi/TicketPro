import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { Contract } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { FileText, Calendar, DollarSign } from 'lucide-react';

export function ContractListPage() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadContracts();
  }, []);

  const loadContracts = async () => {
    setLoading(true);
    try {
      const data = await api.getContracts();
      setContracts(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const columns: Column<Contract>[] = [
    { key: 'contract_number', header: 'Contract #', render: (c) => <span className="font-semibold text-indigo-600">{c.contract_number}</span> },
    { key: 'title', header: 'Contract Title' },
    { key: 'vendor_name', header: 'Vendor' },
    { key: 'contract_type', header: 'Type' },
    { key: 'annual_cost', header: 'Annual Cost', render: (c) => <span className="font-bold text-slate-800">${c.annual_cost ? c.annual_cost.toLocaleString() : 0}</span> },
    { key: 'end_date', header: 'Expiration', render: (c) => <span className="text-xs text-slate-600">{new Date(c.end_date).toLocaleDateString()}</span> },
    { key: 'status', header: 'Status', render: (c) => <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">{c.status}</span> }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <FileText className="h-6 w-6 text-indigo-600" /> Maintenance & Support Contracts
        </h1>
        <p className="text-sm text-slate-500">Track enterprise vendor SLAs, warranty renewals, and support contract terms.</p>
      </div>
      {loading ? <div className="py-12 text-center text-slate-400">Loading support contracts...</div> : <DataTable columns={columns} data={contracts} />}
    </div>
  );
}
