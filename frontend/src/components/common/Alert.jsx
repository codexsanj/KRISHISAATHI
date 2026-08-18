import { AlertCircle, CheckCircle2, Info, AlertTriangle } from 'lucide-react'
import { cn } from '../../utils/cn'

const config = {
  info: {
    icon: Info,
    className: 'border-info-border bg-info-bg text-info',
    iconClassName: 'text-info',
  },
  success: {
    icon: CheckCircle2,
    className: 'border-success-border bg-success-bg text-success',
    iconClassName: 'text-success',
  },
  warning: {
    icon: AlertTriangle,
    className: 'border-warning-border bg-warning-bg text-warning',
    iconClassName: 'text-warning',
  },
  danger: {
    icon: AlertCircle,
    className: 'border-danger-border bg-danger-bg text-danger',
    iconClassName: 'text-danger',
  },
}

export function Alert({
  variant = 'info',
  title,
  children,
  className,
  onDismiss,
  ...props
}) {
  const { icon: Icon, className: variantClass, iconClassName } = config[variant]

  return (
    <div
      role="alert"
      className={cn(
        'flex gap-3 rounded-lg border p-4 sm:p-5',
        variantClass,
        className,
      )}
      {...props}
    >
      <Icon
        className={cn('mt-0.5 h-[1.125rem] w-[1.125rem] shrink-0', iconClassName)}
        aria-hidden="true"
      />
      <div className="min-w-0 flex-1">
        {title && <p className="mb-1 text-sm font-semibold">{title}</p>}
        {children && (
          <div className="text-sm leading-relaxed opacity-90">{children}</div>
        )}
      </div>
      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          className="shrink-0 rounded-md p-1 opacity-70 transition-opacity hover:opacity-100"
          aria-label="Dismiss alert"
        >
          ×
        </button>
      )}
    </div>
  )
}
