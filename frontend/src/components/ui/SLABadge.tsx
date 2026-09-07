import React from 'react';
import { formatTimeRemaining } from '../../lib/utils';
import { Clock, AlertOctagon } from 'lucide-react';
import { cn } from '../../lib/utils';

interface SLABadgeProps {
  targetDate?: string;
  isBreached?: boolean;
  label?: string;
  className?: string;
}

export const SLABadge: React.FC<SLABadgeProps> = ({ targetDate, isBreached, label = 'SLA', className }) => {
  if (!targetDate) {
    return (
      <span className="inline-flex items-center text-xs text-text-tertiary">
        <Clock className="w-3 h-3 mr-1" />
        No SLA
      </span>
    );
  }

  const { text, isBreached: computedBreached, isWarning } = formatTimeRemaining(targetDate);
  const breached = isBreached || computedBreached;

  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border',
        breached
          ? 'bg-danger-light text-danger-dark border-danger/40 font-semibold'
          : isWarning
          ? 'bg-warning-light text-warning-dark border-warning/40'
          : 'bg-surface-subtle text-text-secondary border-border',
        className
      )}
    >
      {breached ? (
        <AlertOctagon className="w-3 h-3 mr-1 text-danger animate-pulse" />
      ) : (
        <Clock className="w-3 h-3 mr-1 text-text-tertiary" />
      )}
      <span>{text}</span>
    </span>
  );
};
