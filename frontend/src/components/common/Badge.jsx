import { cn } from '../../utils/cn'

const variants = {
  default: 'bg-primary-50 text-forest border-primary-200',
  success: 'bg-success-bg text-success border-success-border',
  warning: 'bg-warning-bg text-warning border-warning-border',
  attention: 'bg-attention-bg text-attention border-attention-border',
  danger: 'bg-danger-bg text-danger border-danger-border',
  info: 'bg-info-bg text-info border-info-border',
  weather: 'bg-weather-bg text-weather border-weather-border',
  market: 'bg-market-bg text-market border-market-border',
  pest: 'bg-pest-bg text-pest border-pest-border',
  disease: 'bg-disease-bg text-disease border-disease-border',
  ai: 'bg-ai-bg text-ai border-ai-border',
  neutral: 'bg-surface-muted text-text-muted border-border',
}

export function Badge({
  variant = 'default',
  dot = false,
  className,
  children,
  ...props
}) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 text-xs font-medium leading-normal',
        variants[variant],
        className,
      )}
      {...props}
    >
      {dot && (
        <span
          className="h-1.5 w-1.5 shrink-0 rounded-full bg-current opacity-80"
          aria-hidden="true"
        />
      )}
      {children}
    </span>
  )
}
