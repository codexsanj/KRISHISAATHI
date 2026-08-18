import { AlertCircle } from 'lucide-react'
import { cn } from '../../utils/cn'
import { Button } from './Button'

export function ErrorState({
  title = 'Something went wrong',
  description = 'Please try again in a moment.',
  onRetry,
  className,
  ...props
}) {
  return (
    <div
      role="alert"
      className={cn(
        'surface-card-muted flex flex-col items-center justify-center px-6 py-12 text-center sm:py-16',
        className,
      )}
      {...props}
    >
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-danger-bg text-danger ring-1 ring-danger-border">
        <AlertCircle className="h-6 w-6" aria-hidden="true" />
      </div>
      <h3 className="text-heading-section">{title}</h3>
      <p className="mt-2 max-w-md text-body">{description}</p>
      {onRetry && (
        <div className="mt-6">
          <Button variant="outline" onClick={onRetry}>
            Try again
          </Button>
        </div>
      )}
    </div>
  )
}
