import { ArrowRight } from 'lucide-react'
import { cn } from '../../../utils/cn'
import { Badge } from '../Badge'

export function AdvisoryCard({
  icon: Icon,
  iconLabel,
  title,
  description,
  badge,
  badgeVariant = 'neutral',
  className,
  onClick,
}) {
  const Component = onClick ? 'button' : 'div'

  return (
    <Component
      type={onClick ? 'button' : undefined}
      onClick={onClick}
      className={cn(
        'group w-full overflow-hidden rounded-xl border border-border bg-surface text-left shadow-xs',
        'transition-all duration-200 hover:border-border-strong hover:shadow-sm',
        onClick && 'cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-forest/40',
        className,
      )}
    >
      <div className="flex items-start gap-3 p-4 sm:p-5">
        {Icon && (
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-surface-muted text-text-muted ring-1 ring-border">
            <Icon className="h-4 w-4" aria-hidden="true" />
          </div>
        )}
        <div className="min-w-0 flex-1 space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            {badge && <Badge variant={badgeVariant}>{badge}</Badge>}
            {iconLabel && (
              <span className="text-xs font-medium text-text-subtle">{iconLabel}</span>
            )}
          </div>
          <p className="font-medium text-text">{title}</p>
          <p className="text-body">{description}</p>
        </div>
        <ArrowRight
          className="mt-1 h-4 w-4 shrink-0 text-text-subtle transition-transform duration-200 group-hover:translate-x-0.5 group-hover:text-forest"
          aria-hidden="true"
        />
      </div>
    </Component>
  )
}
