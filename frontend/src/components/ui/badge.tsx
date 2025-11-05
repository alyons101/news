import * as React from 'react';

import { cn } from '../../lib/utils';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'outline';
}

export const Badge = ({ className, variant = 'default', ...props }: BadgeProps) => (
  <span
    className={cn(
      'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium',
      variant === 'default' ? 'border-accent/60 bg-accent/10 text-accent' : 'border-slate-700 text-slate-300',
      className
    )}
    {...props}
  />
);
