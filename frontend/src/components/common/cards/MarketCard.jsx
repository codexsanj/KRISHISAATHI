import { ArrowRight, TrendingUp } from 'lucide-react'
import { cn } from '../../../utils/cn'
import { Badge } from '../Badge'

export function MarketCard({
  icon: Icon = TrendingUp,
  crop,
  price,
  trend,
  description,
  className,
  onClick,
}) {
  const Component = onClick ? 'button' : 'div'

  return (
    <Component
      type={onClick ? 'button' : undefined}
      onClick={onClick}
      className={cn(
        'group w-full overflow-hidden rounded-xl border border-market-border bg-market-bg/50 text-left shadow-xs',
        'transition-all duration-200 hover:border-market/30 hover:shadow-sm',
        onClick && 'cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-market/40',
        className,
      )}
    >
      <div className="p-4 sm:p-5">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-market/10 text-market ring-1 ring-market/20">
              <Icon className="h-4 w-4" aria-hidden="true" />
            </div>
            <div className="min-w-0 space-y-1">
              <Badge variant="market">Market</Badge>
              {crop && <p className="text-sm font-medium text-text">{crop}</p>}
            </div>
          </div>
          {price && (
            <p className="shrink-0 text-lg font-semibold tracking-tight text-text">{price}</p>
          )}
        </div>
        {description && <p className="mt-3 text-body">{description}</p>}
        {trend && (
          <p
            className={cn(
              'mt-2 text-xs font-medium',
              trend.positive ? 'text-success' : 'text-pest',
            )}
          >
            {trend.label}
          </p>
        )}
        <div className="mt-3 flex items-center gap-1 text-xs font-medium text-market">
          <span>View prices</span>
          <ArrowRight className="h-3.5 w-3.5 transition-transform duration-200 group-hover:translate-x-0.5" />
        </div>
      </div>
    </Component>
  )
}
