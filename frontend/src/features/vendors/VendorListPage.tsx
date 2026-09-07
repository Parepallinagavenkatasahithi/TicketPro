import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { Vendor, SoftwareLicense } from '../../types';
import { DataTable, Column } from '../../components/ui/DataTable';
import { Building2, Key, Star, Plus } from 'lucide-react';

export function VendorListPage() {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [licenses, setLicenses] = useState<SoftwareLicense[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'vendors' | 'licenses'>('vendors');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const v = await api.getVendors();
      const l = await api.getSoftwareLicenses();
      setVendors(v);
      setLicenses(l);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const vendorColumns: Column<Vendor>[] = [
    { key: 'code', header: 'Vendor Code', render: (v) => <span className="font-semibold text-indigo-600">{v.code}</span> },
    { key: 'name', header: 'Vendor Name' },
    { key: 'contact_name', header: 'Primary Contact', render: (v) => <span>{v.contact_name || 'N/A'} ({v.contact_email || '—'})</span> },
    { key: 'rating', header: 'SLA Score', render: (v) => <span className="font-bold text-amber-600">★ {v.rating}</span> }
  ];

  const licenseColumns: Column<SoftwareLicense>[] = [
    { key: 'software_name', header: 'Software Title', render: (l) => <span className="font-semibold text-indigo-600">{l.software_name}</span> },
    { key: 'vendor_name', header: 'Vendor' },
    { key: 'license_type', header: 'License Model' },
    { key: 'allocated_seats', header: 'Seat Allocation', render: (l) => <span>{l.allocated_seats} / {l.total_seats} seats used</span> }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <Building2 className="h-6 w-6 text-indigo-600" /> Vendor & Software License Management
          </h1>
          <p className="text-sm text-slate-500">Directory of third-party vendors, support portals, and SaaS license allocations.</p>
        </div>
      </div>

      <div className="flex gap-2 border-b border-slate-200 dark:border-slate-800">
        <button
          onClick={() => setActiveTab('vendors')}
          className={`pb-2 px-4 font-medium text-sm border-b-2 transition-colors ${
            activeTab === 'vendors' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500'
          }`}
        >
          Vendors ({vendors.length})
        </button>
        <button
          onClick={() => setActiveTab('licenses')}
          className={`pb-2 px-4 font-medium text-sm border-b-2 transition-colors ${
            activeTab === 'licenses' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500'
          }`}
        >
          Software Licenses ({licenses.length})
        </button>
      </div>

      {loading ? (
        <div className="py-12 text-center text-slate-400">Loading vendor records...</div>
      ) : activeTab === 'vendors' ? (
        <DataTable columns={vendorColumns} data={vendors} />
      ) : (
        <DataTable columns={licenseColumns} data={licenses} />
      )}
    </div>
  );
}
