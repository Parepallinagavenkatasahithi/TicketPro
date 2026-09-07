import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { Settings, Share2, Shield, Check } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'general' | 'integrations'>('general');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary tracking-tight">System Settings & Integrations</h1>
        <p className="text-xs text-text-secondary mt-0.5">
          Configure platform defaults, email provider, Slack/Teams webhooks, and routing options
        </p>
      </div>

      <div className="bg-surface rounded-2xl border border-border shadow-card p-6 space-y-6">
        <div className="flex border-b border-border pb-3 space-x-6">
          <button
            onClick={() => setActiveTab('general')}
            className={`text-xs font-bold uppercase tracking-wider pb-2 border-b-2 ${
              activeTab === 'general' ? 'border-brand text-brand-600' : 'border-transparent text-text-tertiary'
            }`}
          >
            General Settings
          </button>
          <button
            onClick={() => setActiveTab('integrations')}
            className={`text-xs font-bold uppercase tracking-wider pb-2 border-b-2 ${
              activeTab === 'integrations' ? 'border-brand text-brand-600' : 'border-transparent text-text-tertiary'
            }`}
          >
            Webhook Integrations
          </button>
        </div>

        {activeTab === 'general' ? (
          <div className="space-y-4 max-w-xl text-xs">
            <div>
              <label className="block font-semibold text-text-secondary mb-1">Organization Name</label>
              <input
                type="text"
                defaultValue="TicketPro Enterprise Corp"
                className="w-full px-3 py-2 bg-surface-subtle border border-border rounded-xl focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-semibold text-text-secondary mb-1">Default SLA Target Hours</label>
              <input
                type="number"
                defaultValue={4}
                className="w-full px-3 py-2 bg-surface-subtle border border-border rounded-xl focus:outline-none"
              />
            </div>
            <button className="px-4 py-2 bg-brand text-white font-semibold rounded-xl hover:bg-brand-600">
              Save Settings
            </button>
          </div>
        ) : (
          <div className="space-y-4 text-xs">
            <div className="p-4 rounded-xl border border-border bg-surface-subtle flex items-center justify-between">
              <div>
                <p className="font-bold text-text-primary">Slack IT Operations Webhook</p>
                <p className="text-text-tertiary text-[11px]">Send real-time SLA breach & ticket notifications to #it-alerts</p>
              </div>
              <span className="px-2.5 py-1 rounded-full bg-success-light text-success-dark font-bold text-[10px]">
                ACTIVE
              </span>
            </div>
            <div className="p-4 rounded-xl border border-border bg-surface-subtle flex items-center justify-between">
              <div>
                <p className="font-bold text-text-primary">Microsoft Teams Incident Channel</p>
                <p className="text-text-tertiary text-[11px]">Webhook integration for critical security incident alerts</p>
              </div>
              <span className="px-2.5 py-1 rounded-full bg-gray-100 text-gray-700 font-bold text-[10px]">
                INACTIVE
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
