import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { Announcement } from '../../types';
import { Megaphone, Calendar, User as UserIcon, Plus } from 'lucide-react';
import { formatDate } from '../../lib/utils';

export const AnnouncementListPage: React.FC = () => {
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);

  useEffect(() => {
    apiFetch<Announcement[]>('/announcements')
      .then((data) => setAnnouncements(data || []))
      .catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary tracking-tight">Company Announcements</h1>
          <p className="text-xs text-text-secondary mt-0.5">
            System maintenance notices, IT policy updates, and operational bulletins
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {announcements.map((a) => (
          <div key={a.id} className="bg-surface p-6 rounded-2xl border border-border shadow-card space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                  a.priority === 'URGENT' ? 'bg-danger-light text-danger-dark' :
                  a.priority === 'IMPORTANT' ? 'bg-warning-light text-warning-dark' :
                  'bg-brand-50 text-brand-700'
                }`}>
                  {a.priority}
                </span>
                <h3 className="text-base font-bold text-text-primary">{a.title}</h3>
              </div>
              <span className="text-xs text-text-tertiary">{formatDate(a.created_at)}</span>
            </div>

            <p className="text-xs text-text-secondary leading-relaxed whitespace-pre-line">{a.content}</p>

            <div className="flex items-center space-x-4 pt-3 border-t border-border text-xs text-text-tertiary">
              <span>Published by: <strong className="text-text-secondary">{a.author_name}</strong></span>
              <span>Target: <strong className="text-text-secondary">{a.target_audience}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
