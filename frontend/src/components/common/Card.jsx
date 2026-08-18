import { cn } from '../../utils/cn'

const accentStyles = {
  default: '',
  primary: 'border-l-[3px] border-l-forest',
  weather: 'border-l-[3px] border-l-weather',
  market: 'border-l-[3px] border-l-market',
  irrigation: 'border-l-[3px] border-l-irrigation',
  ai: 'border-l-[3px] border-l-ai',
  success: 'border-l-[3px] border-l-success',
  warning: 'border-l-[3px] border-l-attention',
  pest: 'border-l-[3px] border-l-pest',
  danger: 'border-l-[3px] border-l-disease',
}

export function Card({
  className,
  children,
  accent = 'default',
  as: Component = 'div',
  ...props
}) {
  return (
    <Component
      className={cn(
        'surface-card overflow-hidden transition-shadow duration-200 hover:shadow-sm',
        accentStyles[accent],
        className,
      )}
      {...props}
    >
      {children}
    </Component>
  )
}

export function CardHeader({ className, children, ...props }) {
  return (
    <div className={cn('px-4 pt-4 pb-2 sm:px-5 sm:pt-5 sm:pb-3', className)} {...props}>
      {children}
    </div>
  )
}

export function CardBody({ className, children, ...props }) {
  return (
    <div className={cn('px-4 pb-4 sm:px-5 sm:pb-5', className)} {...props}>
      {children}
    </div>
  )
}

export function CardFooter({ className, children, ...props }) {
  return (
    <div
      className={cn(
        'flex items-center gap-3 border-t border-border px-4 py-3 sm:px-5 sm:py-4',
        className,
      )}
      {...props}
    >
      {children}
    </div>
  )
}
