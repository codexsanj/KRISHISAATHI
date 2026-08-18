import { Sprout } from 'lucide-react'
import { cn } from '../../utils/cn'

export function BrandMark({ showTagline = true, size = 'md', inverted = false, className }) {
  const sizes = {
    sm: { icon: 'h-4 w-4', box: 'h-8 w-8', title: 'text-sm', tagline: 'text-[10px]' },
    md: { icon: 'h-[1.125rem] w-[1.125rem]', box: 'h-9 w-9', title: 'text-sm', tagline: 'text-xs' },
    lg: { icon: 'h-5 w-5', box: 'h-10 w-10', title: 'text-base', tagline: 'text-xs' },
  }

  const s = sizes[size]

  return (
    <div className={cn('flex min-w-0 items-center gap-3', className)}>
      <div
        className={cn(
          'flex shrink-0 items-center justify-center rounded-lg shadow-xs ring-1',
          inverted
            ? 'bg-white/15 text-text-inverse ring-white/20'
            : 'bg-forest text-text-inverse ring-forest/20',
          s.box,
        )}
      >
        <Sprout className={s.icon} aria-hidden="true" />
      </div>
      <div className="min-w-0">
        <p className={cn('truncate font-semibold tracking-tight', inverted ? 'text-text-inverse' : 'text-text', s.title)}>
          KrishiSaathi
        </p>
        {showTagline && (
          <p className={cn('truncate', inverted ? 'text-sage-light/90' : 'text-sage-dark', s.tagline)}>
            Smart Crop Advisory
          </p>
        )}
      </div>
    </div>
  )
}
