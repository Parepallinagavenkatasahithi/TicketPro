import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  LayoutDashboard, Ticket, FileText, PlusCircle, Layers, CheckSquare,
  Megaphone, Users, Building2, ShieldCheck, BarChart3, BookOpen,
  Clock, History, Settings, Share2, HardDrive, LogOut, ChevronLeft, ChevronRight
} from 'lucide-react';
import { cn } from '../../lib/utils';

interface SidebarProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
  onCreateTicketClick: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ collapsed, onToggleCollapse, onCreateTicketClick }) => {
  const { user, logout, hasPermission } = useAuth();
  const navigate = useNavigate();

  const mainNav = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, permission: 'ticket.view' },
    { label: 'My Tickets', path: '/my-tickets', icon: FileText, permission: 'ticket.view' },
    { label: 'All Tickets', path: '/tickets', icon: Ticket, permission: 'ticket.view' },
    { label: 'Approvals', path: '/approvals', icon: CheckSquare, permission: 'ticket.view' },
    { label: 'Announcements', path: '/announcements', icon: Megaphone, permission: 'ticket.view' },
  ];

  const managementNav = [
    { label: 'Employees', path: '/employees', icon: Users, permission: 'employee.view' },
    { label: 'Departments', path: '/departments', icon: Building2, permission: 'department.manage' },
    { label: 'Roles & Permissions', path: '/roles', icon: ShieldCheck, permission: 'settings.manage' },
  ];

  const itilNav = [
    { label: 'Asset Management', path: '/assets', icon: HardDrive, permission: 'ticket.view' },
    { label: 'Change Management', path: '/change-requests', icon: Layers, permission: 'ticket.view' },
    { label: 'Problem Management', path: '/problems', icon: ShieldCheck, permission: 'ticket.view' },
    { label: 'CSAT Ratings', path: '/surveys', icon: BarChart3, permission: 'ticket.view' },
    { label: 'Time Tracking', path: '/time-tracking', icon: Clock, permission: 'ticket.view' },
    { label: 'Vendors & SaaS', path: '/vendors', icon: Building2, permission: 'ticket.view' },
    { label: 'Support Contracts', path: '/contracts', icon: FileText, permission: 'ticket.view' },
    { label: 'On-Call Roster', path: '/on-call', icon: Users, permission: 'ticket.view' },
    { label: 'Service Catalog', path: '/service-catalog', icon: PlusCircle, permission: 'ticket.view' },
    { label: 'Custom Fields', path: '/custom-fields', icon: Settings, permission: 'settings.manage' },
    { label: 'Email Templates', path: '/email-templates', icon: Megaphone, permission: 'settings.manage' },
  ];

  const systemNav = [
    { label: 'Reports & Analytics', path: '/analytics', icon: BarChart3, permission: 'reports.view' },
    { label: 'Knowledge Base', path: '/knowledge-base', icon: BookOpen, permission: 'kb.view' },
    { label: 'SLA Management', path: '/sla', icon: Clock, permission: 'sla.view' },
    { label: 'Audit Logs', path: '/audit', icon: History, permission: 'audit.view' },
    { label: 'Settings', path: '/settings', icon: Settings, permission: 'settings.manage' },
    { label: 'Integrations', path: '/integrations', icon: Share2, permission: 'settings.manage' },
  ];

  return (
    <aside
      className={cn(
        'fixed top-0 left-0 z-40 h-screen bg-surface border-r border-border flex flex-col justify-between transition-all duration-300',
        collapsed ? 'w-20' : 'w-64'
      )}
    >
      {/* Brand Header */}
      <div>
        <div className="flex items-center justify-between p-4 border-b border-border">
          <div className="flex items-center space-x-3 overflow-hidden">
            <div className="w-10 h-10 rounded-xl bg-brand flex items-center justify-center text-white shadow-md flex-shrink-0">
              <Ticket className="w-6 h-6" />
            </div>
            {!collapsed && (
              <div className="flex flex-col truncate">
                <span className="font-bold text-lg text-text-primary tracking-tight leading-none">TicketPro</span>
                <span className="text-[10px] text-text-tertiary font-medium mt-1 truncate">IT Operations Platform</span>
              </div>
            )}
          </div>
          <button
            onClick={onToggleCollapse}
            className="p-1 rounded-lg text-text-tertiary hover:bg-surface-subtle hover:text-text-primary"
          >
            {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
          </button>
        </div>

        {/* Quick Action Button */}
        <div className="p-3">
          <button
            onClick={onCreateTicketClick}
            className={cn(
              'w-full flex items-center justify-center space-x-2 py-2.5 px-3 rounded-xl bg-brand text-white font-semibold text-sm shadow-sm hover:bg-brand-600 transition-colors',
              collapsed && 'px-0'
            )}
          >
            <PlusCircle className="w-5 h-5" />
            {!collapsed && <span>Create Ticket</span>}
          </button>
        </div>

        {/* Navigation Items */}
        <div className="px-3 py-2 space-y-6 overflow-y-auto max-h-[calc(100vh-250px)]">
          {/* Main Group */}
          <div className="space-y-1">
            {mainNav.filter(item => hasPermission(item.permission)).map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  cn(
                    'flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-brand-50 text-brand-600 font-semibold'
                      : 'text-text-secondary hover:bg-surface-subtle hover:text-text-primary'
                  )
                }
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                {!collapsed && <span>{item.label}</span>}
              </NavLink>
            ))}
          </div>

          {/* Management Group */}
          {managementNav.some(i => hasPermission(i.permission)) && (
            <div>
              {!collapsed && (
                <div className="px-3 text-[11px] font-bold uppercase tracking-wider text-text-tertiary mb-2">
                  Management
                </div>
              )}
              <div className="space-y-1">
                {managementNav.filter(item => hasPermission(item.permission)).map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      cn(
                        'flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                        isActive
                          ? 'bg-brand-50 text-brand-600 font-semibold'
                          : 'text-text-secondary hover:bg-surface-subtle hover:text-text-primary'
                      )
                    }
                  >
                    <item.icon className="w-5 h-5 flex-shrink-0" />
                    {!collapsed && <span>{item.label}</span>}
                  </NavLink>
                ))}
              </div>
            </div>
          )}

          {/* ITIL Operations Group */}
          {itilNav.some(i => hasPermission(i.permission)) && (
            <div>
              {!collapsed && (
                <div className="px-3 text-[11px] font-bold uppercase tracking-wider text-text-tertiary mb-2">
                  ITIL Operations
                </div>
              )}
              <div className="space-y-1">
                {itilNav.filter(item => hasPermission(item.permission)).map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      cn(
                        'flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                        isActive
                          ? 'bg-brand-50 text-brand-600 font-semibold'
                          : 'text-text-secondary hover:bg-surface-subtle hover:text-text-primary'
                      )
                    }
                  >
                    <item.icon className="w-5 h-5 flex-shrink-0" />
                    {!collapsed && <span>{item.label}</span>}
                  </NavLink>
                ))}
              </div>
            </div>
          )}

          {/* System Group */}
          {systemNav.some(i => hasPermission(i.permission)) && (
            <div>
              {!collapsed && (
                <div className="px-3 text-[11px] font-bold uppercase tracking-wider text-text-tertiary mb-2">
                  System
                </div>
              )}
              <div className="space-y-1">
                {systemNav.filter(item => hasPermission(item.permission)).map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) =>
                      cn(
                        'flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                        isActive
                          ? 'bg-brand-50 text-brand-600 font-semibold'
                          : 'text-text-secondary hover:bg-surface-subtle hover:text-text-primary'
                      )
                    }
                  >
                    <item.icon className="w-5 h-5 flex-shrink-0" />
                    {!collapsed && <span>{item.label}</span>}
                  </NavLink>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Bottom Footer Widget */}
      <div className="p-3 border-t border-border space-y-3">
        {!collapsed && (
          <div className="bg-surface-subtle p-3 rounded-xl space-y-1.5 border border-border/50">
            <div className="flex items-center justify-between text-xs text-text-secondary font-medium">
              <span className="flex items-center">
                <HardDrive className="w-3.5 h-3.5 mr-1.5 text-brand-500" />
                Storage Usage
              </span>
              <span>4.2 GB / 50 GB</span>
            </div>
            <div className="w-full bg-border rounded-full h-1.5 overflow-hidden">
              <div className="bg-brand h-full rounded-full" style={{ width: '8.4%' }} />
            </div>
          </div>
        )}

        {/* Current User Card */}
        <div className="flex items-center justify-between p-2 rounded-xl hover:bg-surface-subtle">
          <div className="flex items-center space-x-3 overflow-hidden">
            <div className="w-9 h-9 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-sm flex-shrink-0">
              {user?.full_name?.charAt(0) || 'U'}
            </div>
            {!collapsed && (
              <div className="flex flex-col truncate">
                <span className="text-sm font-semibold text-text-primary truncate">{user?.full_name}</span>
                <span className="text-xs text-text-tertiary capitalize">{user?.role_name}</span>
              </div>
            )}
          </div>
          {!collapsed && (
            <button
              onClick={logout}
              title="Logout"
              className="p-1.5 rounded-lg text-text-tertiary hover:text-danger hover:bg-danger-light"
            >
              <LogOut className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
};
