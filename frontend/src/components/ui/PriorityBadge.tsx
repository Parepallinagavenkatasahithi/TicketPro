import React from 'react';
import { TicketPriorityType } from '../../types';
import { cn } from '../../lib/utils';
import { AlertCircle, AlertTriangle, ArrowUp, ArrowDown } from 'lucide-react';

interface PriorityBadgeProps {
  priority: TicketPriorityType | string;
  showIcon?: boolean;
  className?: string;
}

export const PriorityBadge: React.FC<PriorityBadgeProps> = ({ priority, showIcon = true, className }) => {
  const normalized = priority.toUpperCase();

  const getStyle = () => {
    switch (normalized) {
      case 'CRITICAL':
        return 'bg-red-100 text-red-800 border-red-300 font-bold';
      case 'HIGH':
        return 'bg-danger-light text-danger-dark border-danger/30';
      case 'MEDIUM':
        return 'bg-warning-light text-warning-dark border-warning/30';
      case 'LOW':
        return 'bg-success-light text-success-dark border-success/30';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const renderIcon = () => {
    if (!showIcon) return null;
    switch (normalized) {
      case 'CRITICAL':
        return <AlertCircle className="w-3 h-3 mr-1 text-red-700 animate-pulse" />;
      case 'HIGH':
        return <AlertTriangle className="w-3 h-3 mr-1 text-danger" />;
      case 'MEDIUM':
        return <ArrowUp className="w-3 h-3 mr-1 text-warning-dark" />;
      case 'LOW':
        return <ArrowDown className="w-3 h-3 mr-1 text-success-dark" />;
      default:
        return null;
    }
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium border',
        getStyle(),
        className
      )}
    >
      {renderIcon()}
      {normalized}
    </span>
  );
};
