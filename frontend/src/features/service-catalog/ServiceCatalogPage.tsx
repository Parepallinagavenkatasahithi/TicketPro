import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { ServiceCatalogItem, ServiceCatalogCategory } from '../../types';
import { Package, ArrowRight, ShieldCheck, Clock } from 'lucide-react';

export function ServiceCatalogPage() {
  const [categories, setCategories] = useState<ServiceCatalogCategory[]>([]);
  const [items, setItems] = useState<ServiceCatalogItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCatalog();
  }, []);

  const loadCatalog = async () => {
    setLoading(true);
    try {
      const c = await api.getServiceCatalogCategories();
      const i = await api.getServiceCatalogItems();
      setCategories(c);
      setItems(i);
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
          <Package className="h-6 w-6 text-indigo-600" /> Employee IT Service Catalog
        </h1>
        <p className="text-sm text-slate-500">Self-service catalog for software access, hardware requests, and account provisioning.</p>
      </div>

      {loading ? (
        <div className="py-12 text-center text-slate-400">Loading IT service catalog items...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {items.map((item) => (
            <div key={item.id} className="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-xs font-semibold bg-indigo-100 text-indigo-800">{item.category_name || 'Service'}</span>
                  {item.requires_approval && (
                    <span className="inline-flex items-center gap-1 text-xs text-amber-600 font-semibold"><ShieldCheck className="h-3.5 w-3.5" /> Approval Required</span>
                  )}
                </div>
                <h3 className="font-bold text-slate-900 dark:text-slate-100 text-base mb-1">{item.name}</h3>
                <p className="text-xs text-slate-500 mb-4">{item.short_description}</p>
              </div>

              <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs">
                <span className="flex items-center gap-1 text-slate-400"><Clock className="h-3.5 w-3.5" /> SLA: {item.estimated_fulfillment_hours}h</span>
                <button className="font-semibold text-indigo-600 hover:text-indigo-700 flex items-center gap-1">
                  Request Service <ArrowRight className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
