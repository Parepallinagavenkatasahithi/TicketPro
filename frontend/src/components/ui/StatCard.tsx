import React from 'react';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
import { cn } from '../../lib/utils';

interface StatCardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  trendPercentage?: number;
  trendLabel?: string;
  iconColor?: string;
  bgColor?: string;
  className?: string;
  onClick?: () => void;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon: Icon,
  trendPercentage,
  trendLabel = 'from last week',
  iconColor = 'text-brand-500',
  bgColor = 'bg-brand-50',
  className,
  onClick,
}) => {
  const isPositive = trendPercentage && trendPercentage > 0;
  const isNegative = trendPercentage && trendPercentage < 0;

  return (
    <div
      onClick={onClick}
      className={cn(
        'bg-surface p-5 rounded-xl border border-border shadow-card transition-all duration-200 hover:shadow-card-hover',
        onClick && 'cursor-pointer hover:border-brand-300',
        className
      )}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-text-secondary">{title}</span>
        <div className={cn('p-2.5 rounded-lg flex items-center justify-center', bgColor)}>
          <Icon className={cn('w-5 h-5', iconColor)} />
        </div>
      </div>
      <div className="mt-3 flex items-baseline justify-between">
        <span className="text-2xl font-bold tracking-tight text-text-primary">{value}</span>
        {trendPercentage !== undefined && (
          <div
            className={cn(
              'inline-flex items-center text-xs font-semibold rounded-full px-2 py-0.5',
              isPositive ? 'bg-success-light text-success-dark' : 'bg-danger-light text-danger-dark'
            )}
          >
            {isPositive ? (
              <TrendingUp className="w-3 h-3 mr-1" />
            ) : (
              <TrendingDown className="w-3 h-3 mr-1" />
            )}
            {Math.abs(trendPercentage)}%
          </div>
        )}
      </div>
      {trendLabel && (
        <p className="mt-1 text-xs text-text-tertiary">{trendLabel}</p>
      )}
    </div>
  );
};
