import { cn } from '../../utils/cn'

const accentStyles = {
  default: 'bg-primary-50 text-forest',
  weather: 'bg-weather-bg text-weather',
  market: 'bg-market-bg text-market',
  irrigation: 'bg-irrigation-bg text-irrigation',
  ai: 'bg-ai-bg text-ai',
  success: 'bg-success-bg text-success',
  warning: 'bg-attention-bg text-attention',
  danger: 'bg-pest-bg text-pest',
}

export function StatCard({
  label,
  value,
  hint,
  icon: Icon,
  trend,
  accent = 'default',
  className,
  ...props
}) {
  return (
    <div
      className={cn(
        'surface-card p-4 transition-shadow duration-200 hover:shadow-sm sm:p-4',
        className,
      )}
      {...props}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-label normal-case tracking-normal">{label}</p>
          <p className="mt-1 text-xl font-semibold tracking-tight text-text sm:text-2xl">
            {value}
          </p>
          {hint && <p className="mt-0.5 text-xs text-text-subtle">{hint}</p>}
        </div>
        {Icon && (
          <div
            className={cn(
              'flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ring-1 ring-inset ring-black/5',
              accentStyles[accent],
            )}
          >
            <Icon className="h-4 w-4" aria-hidden="true" />
          </div>
        )}
      </div>
      {trend && (
        <p
          className={cn(
            'mt-2.5 border-t border-border pt-2.5 text-xs font-medium',
            trend.positive ? 'text-success' : 'text-pest',
          )}
        >
          {trend.label}
        </p>
      )}
    </div>
  )
}
