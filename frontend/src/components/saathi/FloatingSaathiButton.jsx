import { Link, useLocation } from 'react-router-dom'
import { Sparkles } from 'lucide-react'
import { cn } from '../../utils/cn'

export function FloatingSaathiButton() {
  const { pathname } = useLocation()
  const isOnSaathiPage = pathname === '/saathi'

  if (isOnSaathiPage) return null

  return (
    <Link
      to="/saathi"
      className={cn(
        'saathi-fab fixed z-30 flex items-center gap-2 rounded-full bg-forest px-4 py-3 text-sm font-medium text-text-inverse shadow-md',
        'transition-all duration-200 hover:bg-forest-dark hover:shadow-lg',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-forest focus-visible:ring-offset-2',
        /* Desktop */
        'right-6 bottom-6',
        /* Mobile — above bottom nav */
        'max-lg:right-4 max-lg:bottom-[calc(4rem+env(safe-area-inset-bottom))] max-lg:px-3.5 max-lg:py-2.5',
      )}
      aria-label="Ask Saathi"
    >
      <span className="saathi-glow flex h-7 w-7 items-center justify-center rounded-full bg-white/15">
        <Sparkles className="h-4 w-4" aria-hidden="true" />
      </span>
      <span className="max-sm:hidden">Ask Saathi</span>
    </Link>
  )
}
