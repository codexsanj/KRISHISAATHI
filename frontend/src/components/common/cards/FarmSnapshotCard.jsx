import { cn } from '../../../utils/cn'

const accentStyles = {
  weather: {
    card: 'border-weather-border/60 bg-weather-bg/40 hover:border-weather/30',
    icon: 'bg-weather/10 text-weather ring-weather/20',
  },
  irrigation: {
    card: 'border-irrigation-border/60 bg-irrigation-bg/40 hover:border-irrigation/30',
    icon: 'bg-irrigation/10 text-irrigation ring-irrigation/20',
  },
  health: {
    card: 'border-success-border/60 bg-success-bg/40 hover:border-success/30',
    icon: 'bg-success/10 text-success ring-success/20',
  },
  market: {
    card: 'border-market-border/60 bg-market-bg/40 hover:border-market/30',
    icon: 'bg-market/10 text-market ring-market/20',
  },
}

export function FarmSnapshotCard({
  icon: Icon,
  category,
  value,
  label,
  detail,
  accent = 'weather',
  className,
}) {
  const styles = accentStyles[accent]

  return (
    <div
      className={cn(
        'overflow-hidden rounded-xl border shadow-xs transition-all duration-200 hover:shadow-sm',
        styles.card,
        className,
      )}
    >
      <div className="p-3.5 sm:p-4">
        <div className="flex items-start justify-between gap-2">
          <div
            className={cn(
              'flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ring-1',
              styles.icon,
            )}
          >
            <Icon className="h-4 w-4" aria-hidden="true" />
          </div>
          <span className="text-label text-[10px]">{category}</span>
        </div>
        <p className="mt-2.5 text-xl font-semibold tracking-tight text-text">{value}</p>
        <p className="mt-0.5 text-sm font-medium text-text">{label}</p>
        {detail && <p className="mt-1 text-xs text-text-muted">{detail}</p>}
      </div>
    </div>
  )
}
