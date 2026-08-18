import { cn } from '../../utils/cn'

const variants = {
  primary:
    'bg-forest text-text-inverse hover:bg-forest-dark active:bg-primary-900 border border-transparent shadow-xs',
  secondary:
    'bg-surface text-text border border-border hover:bg-surface-muted active:bg-surface-subtle',
  outline:
    'bg-transparent text-text border border-border hover:bg-surface-muted active:bg-surface-subtle',
  ghost:
    'bg-transparent text-text-muted border border-transparent hover:bg-surface-muted hover:text-forest',
  danger:
    'bg-danger text-text-inverse hover:bg-red-700 active:bg-red-800 border border-transparent',
}

const sizes = {
  sm: 'h-9 px-3.5 text-sm gap-1.5 rounded-md',
  md: 'h-11 px-4 text-sm gap-2 rounded-md',
  lg: 'h-12 px-5 text-base gap-2.5 rounded-md',
  icon: 'h-11 w-11 p-0 rounded-md',
}

export function Button({
  variant = 'primary',
  size = 'md',
  className,
  children,
  leftIcon: LeftIcon,
  rightIcon: RightIcon,
  isLoading = false,
  disabled,
  ...props
}) {
  return (
    <button
      type="button"
      className={cn(
        'inline-flex items-center justify-center font-medium transition-colors duration-150',
        'disabled:pointer-events-none disabled:opacity-50',
        'touch-manipulation select-none',
        variants[variant],
        sizes[size],
        className,
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span
          className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
          aria-hidden="true"
        />
      ) : (
        LeftIcon && <LeftIcon className="h-4 w-4 shrink-0" aria-hidden="true" />
      )}
      {children}
      {!isLoading && RightIcon && (
        <RightIcon className="h-4 w-4 shrink-0" aria-hidden="true" />
      )}
    </button>
  )
}
