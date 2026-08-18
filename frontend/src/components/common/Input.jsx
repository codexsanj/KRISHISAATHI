import { cn } from '../../utils/cn'

export function Input({
  label,
  hint,
  error,
  id,
  className,
  wrapperClassName,
  ...props
}) {
  const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined)

  return (
    <div className={cn('w-full', wrapperClassName)}>
      {label && (
        <label htmlFor={inputId} className="input-label">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={cn(
          'input-field',
          error && 'border-danger focus:border-danger focus:shadow-[0_0_0_3px_rgb(181_69_58_/_0.12)]',
          className,
        )}
        aria-invalid={error ? 'true' : undefined}
        aria-describedby={hint || error ? `${inputId}-desc` : undefined}
        {...props}
      />
      {(hint || error) && (
        <p
          id={`${inputId}-desc`}
          className={cn('input-hint', error && 'text-danger')}
        >
          {error || hint}
        </p>
      )}
    </div>
  )
}
