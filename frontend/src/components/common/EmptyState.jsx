import { cn } from '../../utils/cn'

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  className,
  ...props
}) {
  return (
    <div
      className={cn(
        'surface-card-muted flex flex-col items-center justify-center px-5 py-10 text-center sm:py-14',
        className,
      )}
      {...props}
    >
      {Icon && (
        <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-lg bg-primary-50 text-forest ring-1 ring-primary-200/60">
          <Icon className="h-5 w-5" aria-hidden="true" />
        </div>
      )}
      <h3 className="text-heading-section">{title}</h3>
      {description && (
        <p className="mt-1.5 max-w-md text-body">{description}</p>
      )}
      {action && <div className="mt-5">{action}</div>}
    </div>
  )
}
