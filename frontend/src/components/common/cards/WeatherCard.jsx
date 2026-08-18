import { ArrowRight, CloudSun } from 'lucide-react'
import { cn } from '../../../utils/cn'
import { Badge } from '../Badge'

export function WeatherCard({
  icon: Icon = CloudSun,
  title = 'Weather advisory',
  description,
  detail,
  className,
  onClick,
}) {
  const Component = onClick ? 'button' : 'div'

  return (
    <Component
      type={onClick ? 'button' : undefined}
      onClick={onClick}
      className={cn(
        'group w-full overflow-hidden rounded-xl border border-weather-border bg-weather-bg/50 text-left shadow-xs',
        'transition-all duration-200 hover:border-weather/30 hover:shadow-sm',
        onClick && 'cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-weather/40',
        className,
      )}
    >
      <div className="flex items-start gap-3 p-4 sm:p-5">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-weather/10 text-weather ring-1 ring-weather/20">
          <Icon className="h-4 w-4" aria-hidden="true" />
        </div>
        <div className="min-w-0 flex-1 space-y-2">
          <Badge variant="weather">Weather</Badge>
          <p className="font-medium text-text">{title}</p>
          <p className="text-body">{description}</p>
          {detail && <p className="text-xs font-medium text-weather">{detail}</p>}
        </div>
        <ArrowRight
          className="mt-1 h-4 w-4 shrink-0 text-weather/60 transition-transform duration-200 group-hover:translate-x-0.5"
          aria-hidden="true"
        />
      </div>
    </Component>
  )
}
