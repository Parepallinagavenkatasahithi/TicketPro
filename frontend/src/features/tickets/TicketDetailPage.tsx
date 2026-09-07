import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { apiFetch } from '../../services/api';
import { TicketDetail, User } from '../../types';
import { TicketStatusBadge } from '../../components/ui/TicketStatusBadge';
import { PriorityBadge } from '../../components/ui/PriorityBadge';
import { SLABadge } from '../../components/ui/SLABadge';
import {
  ArrowLeft, Clock, User as UserIcon, Send, Lock, Paperclip,
  CheckCircle, RefreshCw, AlertTriangle, ShieldAlert, FileText, History
} from 'lucide-react';
import { formatDate, formatTimeAgo, formatFileSize } from '../../lib/utils';

export const TicketDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user, hasPermission } = useAuth();
  const navigate = useNavigate();

  const [ticket, setTicket] = useState<TicketDetail | null>(null);
  const [agents, setAgents] = useState<User[]>([]);
  const [activeTab, setActiveTab] = useState<'comments' | 'timeline' | 'attachments'>('comments');
  const [commentText, setCommentText] = useState('');
  const [isInternalNote, setIsInternalNote] = useState(false);
  const [selectedAgentId, setSelectedAgentId] = useState<number | ''>('');
  const [selectedStatus, setSelectedStatus] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [submittingComment, setSubmittingComment] = useState(false);

  const fetchTicket = async () => {
    if (!id) return;
    try {
      const [tRes, uRes] = await Promise.all([
        apiFetch<TicketDetail>(`/tickets/${id}`),
        apiFetch<User[]>('/users?role=AGENT'),
      ]);
      setTicket(tRes);
      setSelectedStatus(tRes.status);
      setSelectedAgentId(tRes.assigned_agent_id || '');
      setAgents(uRes || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTicket();
  }, [id]);

  if (loading || !ticket) {
    return <div className="p-12 text-center text-xs text-text-tertiary">Loading ticket workspace...</div>;
  }

  const handlePostComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    setSubmittingComment(true);
    try {
      await apiFetch(`/tickets/${ticket.id}/comments`, {
        method: 'POST',
        body: JSON.stringify({
          content: commentText,
          is_internal_note: isInternalNote,
        }),
      });
      setCommentText('');
      fetchTicket();
    } catch (err: any) {
      alert(err.message || 'Failed to post comment');
    } finally {
      setSubmittingComment(false);
    }
  };

  const handleStatusChange = async (newStatus: string) => {
    try {
      await apiFetch(`/tickets/${ticket.id}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status: newStatus }),
      });
      fetchTicket();
    } catch (err: any) {
      alert(err.message || 'Status transition failed');
    }
  };

  const handleAssignAgent = async (agentId: number) => {
    try {
      await apiFetch(`/tickets/${ticket.id}/assign`, {
        method: 'PUT',
        body: JSON.stringify({ agent_id: agentId }),
      });
      fetchTicket();
    } catch (err: any) {
      alert(err.message || 'Assignment failed');
    }
  };

  const handleEscalate = async () => {
    try {
      await apiFetch(`/tickets/${ticket.id}/escalate`, { method: 'POST' });
      fetchTicket();
    } catch (err: any) {
      alert(err.message || 'Escalation failed');
    }
  };

  const canPostInternalNotes = user?.role_name !== 'EMPLOYEE';

  return (
    <div className="space-y-6">
      {/* Header & Back button */}
      <div className="flex items-center space-x-3">
        <button
          onClick={() => navigate('/tickets')}
          className="p-2 rounded-xl bg-surface border border-border text-text-secondary hover:text-text-primary shadow-sm"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-sm font-bold text-brand-600">{ticket.ticket_number}</span>
            <TicketStatusBadge status={ticket.status} />
            <PriorityBadge priority={ticket.priority} />
          </div>
          <h1 className="text-xl font-bold text-text-primary tracking-tight mt-0.5">{ticket.title}</h1>
        </div>
      </div>

      {/* Main Workspace Grid (Section 96) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (Main Ticket Body - 2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Ticket Description Card */}
          <div className="bg-surface p-6 rounded-2xl border border-border shadow-card space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-tertiary">Description & Details</h3>
            <p className="text-sm text-text-primary whitespace-pre-line leading-relaxed font-sans">{ticket.description}</p>
            <div className="flex items-center space-x-4 pt-3 border-t border-border text-xs text-text-tertiary">
              <span>Created {formatDate(ticket.created_at)}</span>
              <span>•</span>
              <span>Category: <strong className="text-text-secondary">{ticket.category_name || 'General'}</strong></span>
            </div>
          </div>

          {/* Activity / Comments Workspace */}
          <div className="bg-surface rounded-2xl border border-border shadow-card overflow-hidden">
            {/* Tabs Header */}
            <div className="flex border-b border-border bg-surface-subtle px-4">
              <button
                onClick={() => setActiveTab('comments')}
                className={`py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-colors ${
                  activeTab === 'comments' ? 'border-brand text-brand-600' : 'border-transparent text-text-tertiary hover:text-text-primary'
                }`}
              >
                Conversation ({ticket.comments.length})
              </button>
              <button
                onClick={() => setActiveTab('timeline')}
                className={`py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-colors ${
                  activeTab === 'timeline' ? 'border-brand text-brand-600' : 'border-transparent text-text-tertiary hover:text-text-primary'
                }`}
              >
                Activity Timeline ({ticket.history.length})
              </button>
              <button
                onClick={() => setActiveTab('attachments')}
                className={`py-3 px-4 text-xs font-bold uppercase tracking-wider border-b-2 transition-colors ${
                  activeTab === 'attachments' ? 'border-brand text-brand-600' : 'border-transparent text-text-tertiary hover:text-text-primary'
                }`}
              >
                Attachments ({ticket.attachments.length})
              </button>
            </div>

            {/* Tab Body */}
            <div className="p-6 space-y-6">
              {activeTab === 'comments' && (
                <>
                  {/* Comments Feed */}
                  <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
                    {ticket.comments.map((c) => (
                      <div
                        key={c.id}
                        className={`p-4 rounded-xl border text-xs space-y-2 ${
                          c.is_internal_note
                            ? 'bg-amber-50/60 border-amber-200 text-amber-950'
                            : 'bg-surface-subtle border-border text-text-primary'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <span className="font-bold">{c.author_name}</span>
                            <span className="text-[10px] bg-surface px-2 py-0.5 rounded border border-border text-text-tertiary">
                              {c.author_role}
                            </span>
                            {c.is_internal_note && (
                              <span className="flex items-center text-[10px] font-bold text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">
                                <Lock className="w-3 h-3 mr-1" /> Internal Agent Note
                              </span>
                            )}
                          </div>
                          <span className="text-text-tertiary">{formatTimeAgo(c.created_at)}</span>
                        </div>
                        <p className="text-sm whitespace-pre-line">{c.content}</p>
                      </div>
                    ))}
                  </div>

                  {/* Comment Input Form */}
                  <form onSubmit={handlePostComment} className="pt-4 border-t border-border space-y-3">
                    {canPostInternalNotes && (
                      <div className="flex items-center space-x-2">
                        <label className="flex items-center space-x-2 text-xs font-semibold text-text-secondary cursor-pointer">
                          <input
                            type="checkbox"
                            checked={isInternalNote}
                            onChange={(e) => setIsInternalNote(e.target.checked)}
                            className="rounded border-border text-brand focus:ring-brand"
                          />
                          <span>Post as Agent Internal Note (Hidden from Requester)</span>
                        </label>
                      </div>
                    )}

                    <textarea
                      rows={3}
                      required
                      placeholder={isInternalNote ? 'Write internal agent note...' : 'Write public response to employee...'}
                      value={commentText}
                      onChange={(e) => setCommentText(e.target.value)}
                      className="w-full p-3 bg-surface-subtle border border-border rounded-xl text-xs focus:outline-none focus:border-brand"
                    />

                    <div className="flex justify-end">
                      <button
                        type="submit"
                        disabled={submittingComment}
                        className={`px-4 py-2 rounded-xl text-xs font-semibold text-white flex items-center shadow-sm ${
                          isInternalNote ? 'bg-amber-600 hover:bg-amber-700' : 'bg-brand hover:bg-brand-600'
                        }`}
                      >
                        <Send className="w-3.5 h-3.5 mr-1.5" />
                        {submittingComment ? 'Posting...' : isInternalNote ? 'Save Internal Note' : 'Send Response'}
                      </button>
                    </div>
                  </form>
                </>
              )}

              {/* Timeline Tab */}
              {activeTab === 'timeline' && (
                <div className="space-y-4">
                  {ticket.history.map((h) => (
                    <div key={h.id} className="flex items-start space-x-3 text-xs border-l-2 border-brand-300 pl-4 py-1">
                      <div className="flex-1">
                        <span className="font-bold text-text-primary">{h.actor_name || 'System'}</span>
                        <span className="text-text-secondary ml-2">{h.description}</span>
                      </div>
                      <span className="text-text-tertiary">{formatTimeAgo(h.created_at)}</span>
                    </div>
                  ))}
                </div>
              )}

              {/* Attachments Tab */}
              {activeTab === 'attachments' && (
                <div className="space-y-3">
                  {ticket.attachments.map((att) => (
                    <div key={att.id} className="flex items-center justify-between p-3 rounded-xl bg-surface-subtle border border-border text-xs">
                      <div className="flex items-center space-x-3">
                        <Paperclip className="w-4 h-4 text-brand-500" />
                        <div>
                          <p className="font-medium text-text-primary">{att.file_name}</p>
                          <span className="text-[10px] text-text-tertiary">{formatFileSize(att.file_size)} • Uploaded by {att.uploader_name}</span>
                        </div>
                      </div>
                      <a
                        href={att.storage_path}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs text-brand-600 font-semibold hover:underline"
                      >
                        Download
                      </a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column (Ticket Controls & SLA Sidebar - 1 col) */}
        <div className="space-y-6">
          {/* Quick Actions Panel */}
          <div className="bg-surface p-5 rounded-2xl border border-border shadow-card space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-tertiary">Actions & Controls</h3>

            {/* Change Status */}
            <div>
              <label className="block text-xs font-semibold text-text-secondary mb-1">Ticket Status</label>
              <select
                value={selectedStatus}
                onChange={(e) => {
                  setSelectedStatus(e.target.value);
                  handleStatusChange(e.target.value);
                }}
                className="w-full px-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs font-semibold text-text-primary focus:outline-none"
              >
                <option value="NEW">NEW</option>
                <option value="OPEN">OPEN</option>
                <option value="ASSIGNED">ASSIGNED</option>
                <option value="IN_PROGRESS">IN_PROGRESS</option>
                <option value="WAITING_FOR_USER">WAITING_FOR_USER</option>
                <option value="RESOLVED">RESOLVED</option>
                <option value="CLOSED">CLOSED</option>
                <option value="REOPENED">REOPENED</option>
              </select>
            </div>

            {/* Assign Agent */}
            {hasPermission('ticket.assign') && (
              <div>
                <label className="block text-xs font-semibold text-text-secondary mb-1">Assign Agent</label>
                <select
                  value={selectedAgentId}
                  onChange={(e) => {
                    const agentId = Number(e.target.value);
                    setSelectedAgentId(agentId);
                    handleAssignAgent(agentId);
                  }}
                  className="w-full px-3 py-2 bg-surface-subtle border border-border rounded-xl text-xs font-semibold text-text-primary focus:outline-none"
                >
                  <option value="">Select Agent...</option>
                  {agents.map((a) => (
                    <option key={a.id} value={a.id}>
                      {a.full_name} ({a.department_name || 'IT'})
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Escalate button */}
            {hasPermission('ticket.edit') && (
              <button
                onClick={handleEscalate}
                className="w-full py-2 px-3 rounded-xl bg-danger-light text-danger-dark border border-danger/30 text-xs font-semibold hover:bg-danger/20 transition-colors flex items-center justify-center"
              >
                <AlertTriangle className="w-4 h-4 mr-1.5" /> Escalate Ticket Priority
              </button>
            )}
          </div>

          {/* SLA Status Card (Section 28) */}
          <div className="bg-surface p-5 rounded-2xl border border-border shadow-card space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-tertiary flex items-center">
              <Clock className="w-4 h-4 mr-1.5 text-brand-500" /> SLA Countdown
            </h3>

            <div className="space-y-2 text-xs">
              <div className="p-3 rounded-xl bg-surface-subtle border border-border">
                <span className="text-[10px] uppercase font-bold text-text-tertiary block">First Response Target</span>
                <div className="mt-1">
                  <SLABadge targetDate={ticket.first_response_due_at} isBreached={ticket.first_response_breached} />
                </div>
              </div>

              <div className="p-3 rounded-xl bg-surface-subtle border border-border">
                <span className="text-[10px] uppercase font-bold text-text-tertiary block">Resolution Target</span>
                <div className="mt-1">
                  <SLABadge targetDate={ticket.resolution_due_at} isBreached={ticket.resolution_breached} />
                </div>
              </div>
            </div>
          </div>

          {/* Requester Metadata */}
          <div className="bg-surface p-5 rounded-2xl border border-border shadow-card space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-text-tertiary">Requester Information</h3>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-sm">
                {ticket.requester_name?.charAt(0) || 'U'}
              </div>
              <div>
                <p className="text-xs font-bold text-text-primary">{ticket.requester_name}</p>
                <p className="text-[11px] text-text-tertiary">{ticket.requester_email}</p>
                <span className="text-[10px] font-semibold text-brand-600">{ticket.department_name || 'IT'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
