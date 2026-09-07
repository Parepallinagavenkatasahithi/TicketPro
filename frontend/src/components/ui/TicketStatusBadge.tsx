import React from 'react';
import { TicketStatusType } from '../../types';
import { cn } from '../../lib/utils';

interface TicketStatusBadgeProps {
  status: TicketStatusType | string;
  className?: string;
}

export const TicketStatusBadge: React.FC<TicketStatusBadgeProps> = ({ status, className }) => {
  const normalized = status.toUpperCase();

  const getStyle = () => {
    switch (normalized) {
      case 'NEW':
      case 'OPEN':
        return 'bg-brand-50 text-brand-700 border-brand-200';
      case 'ASSIGNED':
      case 'IN_PROGRESS':
        return 'bg-info-light text-info-dark border-info/30';
      case 'WAITING_FOR_USER':
      case 'WAITING_FOR_APPROVAL':
        return 'bg-warning-light text-warning-dark border-warning/30';
      case 'RESOLVED':
        return 'bg-success-light text-success-dark border-success/30';
      case 'CLOSED':
        return 'bg-gray-100 text-gray-700 border-gray-300';
      case 'REOPENED':
        return 'bg-purple-100 text-purple-800 border-purple-300';
      case 'CANCELLED':
        return 'bg-red-50 text-red-600 border-red-200';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getLabel = () => {
    switch (normalized) {
      case 'IN_PROGRESS': return 'In Progress';
      case 'WAITING_FOR_USER': return 'Waiting on User';
      case 'WAITING_FOR_APPROVAL': return 'Waiting Approval';
      default: return normalized.charAt(0) + normalized.slice(1).toLowerCase();
    }
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border',
        getStyle(),
        className
      )}
    >
      <span className="w-1.5 h-1.5 rounded-full mr-1.5 bg-current opacity-75" />
      {getLabel()}
    </span>
  );
};
