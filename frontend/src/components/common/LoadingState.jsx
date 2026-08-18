import { Loader2 } from 'lucide-react'
import { cn } from '../../utils/cn'

export function LoadingState({
  message = 'Loading…',
  className,
  size = 'md',
  ...props
}) {
  const iconSize = size === 'sm' ? 'h-5 w-5' : 'h-7 w-7'

  return (
    <div
      role="status"
      aria-live="polite"
      className={cn(
        'surface-card-muted flex flex-col items-center justify-center gap-3 px-6 py-14 text-center',
        className,
      )}
      {...props}
    >
      <Loader2
        className={cn('animate-spin text-primary-600', iconSize)}
        aria-hidden="true"
      />
      <p className="text-sm text-text-muted">{message}</p>
    </div>
  )
}
