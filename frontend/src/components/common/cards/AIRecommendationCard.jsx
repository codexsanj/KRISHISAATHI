import { ArrowRight, Sparkles } from 'lucide-react'
import { cn } from '../../../utils/cn'
import { Badge } from '../Badge'

export function AIRecommendationCard({
  icon: Icon = Sparkles,
  title,
  description,
  confidence,
  className,
  onClick,
}) {
  const Component = onClick ? 'button' : 'div'

  return (
    <Component
      type={onClick ? 'button' : undefined}
      onClick={onClick}
      className={cn(
        'group w-full overflow-hidden rounded-xl border border-ai-border bg-ai-bg/40 text-left shadow-xs',
        'transition-all duration-200 hover:border-ai/30 hover:shadow-sm',
        onClick && 'cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ai/40',
        className,
      )}
    >
      <div className="flex items-start gap-3 p-4 sm:p-5">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-ai/10 text-ai ring-1 ring-ai/20">
          <Icon className="h-4 w-4" aria-hidden="true" />
        </div>
        <div className="min-w-0 flex-1 space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="ai">Saathi AI</Badge>
            {confidence && (
              <span className="text-xs text-text-subtle">{confidence} confidence</span>
            )}
          </div>
          <p className="font-medium text-text">{title}</p>
          <p className="text-body">{description}</p>
        </div>
        <ArrowRight
          className="mt-1 h-4 w-4 shrink-0 text-ai/60 transition-transform duration-200 group-hover:translate-x-0.5"
          aria-hidden="true"
        />
      </div>
    </Component>
  )
}
