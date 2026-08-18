import { MapPin, Sprout } from 'lucide-react'
import { cn } from '../../../utils/cn'
import { Badge } from '../Badge'

export function FarmSummaryCard({
  crop,
  area,
  location,
  status = 'Healthy',
  statusVariant = 'success',
  className,
}) {
  return (
    <div
      className={cn(
        'overflow-hidden rounded-xl border border-sage/25 bg-surface shadow-xs',
        className,
      )}
    >
      <div className="flex items-center gap-3 border-b border-border px-4 py-3 sm:px-5">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-sage/15 text-forest ring-1 ring-sage/25">
          <Sprout className="h-4 w-4" aria-hidden="true" />
        </div>
        <div className="min-w-0 flex-1">
          <p className="text-label text-forest">Your farm</p>
          <p className="truncate text-sm font-medium text-text">
            {[crop, area, location].filter(Boolean).join(' · ')}
          </p>
        </div>
        {status && <Badge variant={statusVariant}>{status}</Badge>}
      </div>
      {location && (
        <div className="flex items-center gap-1.5 px-4 py-2.5 text-xs text-text-muted sm:px-5">
          <MapPin className="h-3.5 w-3.5 shrink-0 text-sage-dark" aria-hidden="true" />
          <span className="truncate">{location}</span>
        </div>
      )}
    </div>
  )
}
