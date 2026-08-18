import { ArrowRight, Bug } from 'lucide-react'
import { cn } from '../../../utils/cn'
import { Badge } from '../Badge'

export function RiskCard({
  icon: Icon = Bug,
  riskType = 'Pest risk',
  title,
  description,
  level,
  className,
  onClick,
}) {
  const Component = onClick ? 'button' : 'div'

  return (
    <Component
      type={onClick ? 'button' : undefined}
      onClick={onClick}
      className={cn(
        'group w-full overflow-hidden rounded-xl border border-pest-border bg-pest-bg/60 text-left shadow-xs',
        'transition-all duration-200 hover:border-pest/30 hover:shadow-sm',
        onClick && 'cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-pest/40',
        className,
      )}
    >
      <div className="flex items-start gap-3 p-4 sm:p-5">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-pest/10 text-pest ring-1 ring-pest/20">
          <Icon className="h-4 w-4" aria-hidden="true" />
        </div>
        <div className="min-w-0 flex-1 space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="pest">{riskType}</Badge>
            {level && <span className="text-xs font-medium text-pest">{level}</span>}
          </div>
          <p className="font-medium text-text">{title}</p>
          <p className="text-body">{description}</p>
        </div>
        <ArrowRight
          className="mt-1 h-4 w-4 shrink-0 text-pest/60 transition-transform duration-200 group-hover:translate-x-0.5"
          aria-hidden="true"
        />
      </div>
    </Component>
  )
}
