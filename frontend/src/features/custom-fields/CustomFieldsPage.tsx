import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { CustomField } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { Sliders, Plus, FormInput } from 'lucide-react';

export function CustomFieldsPage() {
  const [fields, setFields] = useState<CustomField[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFields();
  }, []);

  const loadFields = async () => {
    setLoading(true);
    try {
      const data = await api.getCustomFields('TICKET');
      setFields(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const columns: Column<CustomField>[] = [
    { key: 'field_key', header: 'Field Key', render: (f) => <span className="font-mono text-xs text-indigo-600 font-semibold">{f.field_key}</span> },
    { key: 'name', header: 'Label' },
    { key: 'field_type', header: 'Type', render: (f) => <span className="px-2 py-0.5 rounded text-xs font-semibold bg-slate-100 text-slate-700">{f.field_type}</span> },
    { key: 'target_entity', header: 'Entity' },
    { key: 'is_required', header: 'Required', render: (f) => f.is_required ? <span className="text-emerald-600 font-bold">YES</span> : <span className="text-slate-400">NO</span> }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <Sliders className="h-6 w-6 text-indigo-600" /> Dynamic Custom Fields Engine
        </h1>
        <p className="text-sm text-slate-500">Configure dynamic custom form fields and attributes for tickets and assets.</p>
      </div>
      {loading ? <div className="py-12 text-center text-slate-400">Loading custom fields...</div> : <DataTable columns={columns} data={fields} />}
    </div>
  );
}
