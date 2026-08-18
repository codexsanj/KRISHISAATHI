import { cn } from '../../utils/cn'

export function SectionHeader({
  title,
  subtitle,
  eyebrow,
  action,
  compact = false,
  className,
  ...props
}) {
  return (
    <div
      className={cn(
        'flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between',
        compact ? 'gap-1' : 'gap-2',
        className,
      )}
      {...props}
    >
      <div className="min-w-0 space-y-0.5">
        {eyebrow && <p className="text-label">{eyebrow}</p>}
        <h2 className={cn(compact ? 'text-heading-hero' : 'text-heading-page sm:text-2xl')}>
          {title}
        </h2>
        {subtitle && (
          <p className={cn('text-body max-w-2xl', compact ? 'text-xs sm:text-sm' : '')}>
            {subtitle}
          </p>
        )}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  )
}
