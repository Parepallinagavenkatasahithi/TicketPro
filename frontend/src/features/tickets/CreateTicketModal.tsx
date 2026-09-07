import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch } from '../../services/api';
import { TicketCategory, TicketPriorityType, Ticket } from '../../types';
import { X, Upload, Clock, AlertCircle, CheckCircle } from 'lucide-react';
import { PriorityBadge } from '../../components/ui/PriorityBadge';

interface CreateTicketModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export const CreateTicketModal: React.FC<CreateTicketModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState<number | ''>('');
  const [priority, setPriority] = useState<TicketPriorityType>('MEDIUM');
  const [contactMethod, setContactMethod] = useState('EMAIL');
  const [categories, setCategories] = useState<TicketCategory[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (isOpen) {
      apiFetch<TicketCategory[]>('/tickets/categories')
        .then((cats) => {
          setCategories(cats || []);
          if (cats && cats.length > 0) setCategoryId(cats[0].id);
        })
        .catch(console.error);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !description.trim() || !categoryId) {
      setError('Please fill in all required fields');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      // 1. Create ticket
      const ticket = await apiFetch<Ticket>('/tickets', {
        method: 'POST',
        body: JSON.stringify({
          title,
          description,
          category_id: Number(categoryId),
          priority,
          contact_method: contactMethod,
        }),
      });

      // 2. Upload attachment if attached
      if (selectedFile && ticket.id) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        await apiFetch(`/tickets/${ticket.id}/attachments`, {
          method: 'POST',
          body: formData,
        });
      }

      onClose();
      if (onSuccess) onSuccess();
      navigate(`/tickets/${ticket.id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to create ticket');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getSLAEst = () => {
    switch (priority) {
      case 'CRITICAL': return { resp: '15 mins', res: '2 hours' };
      case 'HIGH': return { resp: '30 mins', res: '4 hours' };
      case 'MEDIUM': return { resp: '2 hours', res: '8 hours' };
      case 'LOW': return { resp: '8 hours', res: '24 hours' };
    }
  };

  const slaEst = getSLAEst();

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-text-primary/40 backdrop-blur-sm p-4 sm:p-6 md:p-10 flex items-center justify-center">
      <div className="bg-surface w-full max-w-4xl rounded-2xl shadow-2xl border border-border overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-surface">
          <div>
            <h3 className="text-lg font-bold text-text-primary">Create Support Ticket</h3>
            <p className="text-xs text-text-tertiary">Submit a new IT operations or support request</p>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-text-tertiary hover:bg-surface-subtle hover:text-text-primary">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className="p-6">
          {error && (
            <div className="mb-4 p-3 rounded-xl bg-danger-light border border-danger/30 text-danger-dark text-xs flex items-center">
              <AlertCircle className="w-4 h-4 mr-2 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Desktop Two-Column Layout (Section 56) */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Left Column (Main Form - 2 cols) */}
            <div className="md:col-span-2 space-y-4">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1">
                  Subject / Title <span className="text-danger">*</span>
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Unable to connect to Corporate VPN on macOS"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-surface-subtle border border-border rounded-xl text-sm focus:outline-none focus:border-brand"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1">
                  Issue Description & Steps to Reproduce <span className="text-danger">*</span>
                </label>
                <textarea
                  required
                  rows={6}
                  placeholder="Provide details about the issue, error codes, workstation specs, or impact..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-surface-subtle border border-border rounded-xl text-sm focus:outline-none focus:border-brand font-sans"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1">
                    Category <span className="text-danger">*</span>
                  </label>
                  <select
                    value={categoryId}
                    onChange={(e) => setCategoryId(Number(e.target.value))}
                    className="w-full px-3 py-2.5 bg-surface-subtle border border-border rounded-xl text-sm focus:outline-none focus:border-brand"
                  >
                    {categories.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1">
                    Priority Level <span className="text-danger">*</span>
                  </label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value as TicketPriorityType)}
                    className="w-full px-3 py-2.5 bg-surface-subtle border border-border rounded-xl text-sm focus:outline-none focus:border-brand"
                  >
                    <option value="LOW">Low (Minor issue)</option>
                    <option value="MEDIUM">Medium (Normal work impact)</option>
                    <option value="HIGH">High (Major work blocked)</option>
                    <option value="CRITICAL">Critical (System down)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Right Column (Sidebar Preview & Uploads - 1 col) */}
            <div className="space-y-4 bg-surface-subtle p-4 rounded-xl border border-border/80">
              <h4 className="text-xs font-bold uppercase tracking-wider text-text-tertiary">Ticket & SLA Metadata</h4>

              {/* SLA Target Preview */}
              <div className="p-3 bg-surface rounded-xl border border-border space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-text-secondary">SLA Policy</span>
                  <PriorityBadge priority={priority} />
                </div>
                <div className="text-xs space-y-1 text-text-secondary border-t border-border pt-2">
                  <div className="flex justify-between">
                    <span>First Response:</span>
                    <span className="font-bold text-brand-600">{slaEst.resp}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Target Resolution:</span>
                    <span className="font-bold text-brand-600">{slaEst.res}</span>
                  </div>
                </div>
              </div>

              {/* Contact Method */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1">
                  Preferred Contact
                </label>
                <select
                  value={contactMethod}
                  onChange={(e) => setContactMethod(e.target.value)}
                  className="w-full px-3 py-2 bg-surface border border-border rounded-xl text-xs focus:outline-none"
                >
                  <option value="EMAIL">Email Notification</option>
                  <option value="SLACK">Slack Direct Message</option>
                  <option value="PHONE">Phone Call</option>
                </select>
              </div>

              {/* Attachment File Input */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-text-secondary mb-1">
                  Attach Files (Optional)
                </label>
                <div className="relative border-2 border-dashed border-border rounded-xl p-3 text-center bg-surface hover:border-brand-300 transition-colors">
                  <Upload className="w-5 h-5 mx-auto text-text-tertiary mb-1" />
                  <p className="text-xs text-text-secondary">
                    {selectedFile ? selectedFile.name : 'Drag files or click to browse'}
                  </p>
                  <span className="text-[10px] text-text-tertiary">PNG, JPG, PDF, LOG (Max 10MB)</span>
                  <input
                    type="file"
                    className="absolute inset-0 opacity-0 cursor-pointer"
                    onChange={(e) => {
                      if (e.target.files && e.target.files[0]) {
                        setSelectedFile(e.target.files[0]);
                      }
                    }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Modal Footer */}
          <div className="mt-6 pt-4 border-t border-border flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-sm font-semibold text-text-secondary hover:bg-surface-subtle"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2 rounded-xl text-sm font-semibold text-white bg-brand hover:bg-brand-600 shadow-sm transition-colors"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Ticket'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
