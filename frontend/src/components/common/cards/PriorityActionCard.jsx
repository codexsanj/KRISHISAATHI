import { ArrowRight, Bug } from 'lucide-react'
import { cn } from '../../../utils/cn'
import { Badge } from '../Badge'
import { Button } from '../Button'

export function PriorityActionCard({
  icon: Icon = Bug,
  iconLabel = 'Pest risk',
  title,
  dueLabel,
  what,
  when,
  why,
  ctaLabel = 'View recommendation',
  onCta,
  className,
}) {
  return (
    <article
      className={cn(
        'overflow-hidden rounded-xl border border-pest/20 bg-surface shadow-sm',
        'ring-1 ring-pest/10 transition-all duration-200 hover:border-pest/30 hover:shadow-md',
        className,
      )}
    >
      <div className="border-b border-pest/15 bg-pest-bg/50 px-4 py-3.5 sm:px-5">
        <div className="flex items-start gap-3">
          <div
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-pest/12 text-pest ring-1 ring-pest/20"
            aria-hidden="true"
          >
            <Icon className="h-5 w-5" />
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="pest" dot>{iconLabel}</Badge>
              <span className="text-label text-pest/80">Priority action</span>
            </div>
            <h3 className="mt-1.5 text-lg font-semibold leading-snug tracking-tight text-text sm:text-xl">
              {title}
            </h3>
            {dueLabel && (
              <p className="mt-1 text-sm font-medium text-attention">{dueLabel}</p>
            )}
          </div>
        </div>
      </div>

      <div className="grid gap-0 divide-y divide-border bg-surface sm:grid-cols-3 sm:divide-x sm:divide-y-0">
        <div className="px-4 py-3.5 sm:px-5">
          <p className="text-label mb-1.5 text-forest">What</p>
          <p className="text-sm leading-relaxed text-text">{what}</p>
        </div>
        <div className="px-4 py-3.5 sm:px-5">
          <p className="text-label mb-1.5 text-forest">When</p>
          <p className="text-sm leading-relaxed text-text">{when}</p>
        </div>
        <div className="px-4 py-3.5 sm:px-5">
          <p className="text-label mb-1.5 text-forest">Why</p>
          <p className="text-sm leading-relaxed text-text-muted">{why}</p>
        </div>
      </div>

      {onCta && (
        <div className="border-t border-border bg-surface-muted/40 px-4 py-3 sm:px-5">
          <Button
            variant="ghost"
            size="sm"
            rightIcon={ArrowRight}
            onClick={onCta}
            className="h-auto px-0 text-forest hover:bg-transparent hover:text-forest-dark"
          >
            {ctaLabel}
          </Button>
        </div>
      )}
    </article>
  )
}
