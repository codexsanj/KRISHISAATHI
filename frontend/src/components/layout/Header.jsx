import { NavLink, useLocation } from 'react-router-dom'
import { Bell, Sprout } from 'lucide-react'
import { mainNavItems } from '../../data/navigation'
import { cn } from '../../utils/cn'

const mobileLabels = {
  '/': 'Home',
  '/farm': 'Farm',
  '/health': 'Health',
  '/market': 'Market',
  '/saathi': 'Saathi',
  '/profile': 'Profile',
}

function getPageTitle(pathname) {
  const item = mainNavItems.find(
    (nav) => nav.path === pathname || (nav.path !== '/' && pathname.startsWith(nav.path)),
  )
  return item?.label ?? 'KrishiSaathi'
}

export function Header() {
  const { pathname } = useLocation()
  const pageTitle = getPageTitle(pathname)

  return (
    <header className="sticky top-0 z-30 border-b border-border bg-surface/98">
      <div className="flex h-14 items-center justify-between gap-3 px-3 sm:px-5 lg:h-16 lg:px-8">
        <div className="flex min-w-0 items-center gap-2.5 lg:hidden">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-forest text-text-inverse">
            <Sprout className="h-4 w-4" aria-hidden="true" />
          </div>
          <div className="min-w-0">
            <p className="truncate text-[10px] font-semibold uppercase tracking-wider text-sage-dark">
              KrishiSaathi
            </p>
            <h1 className="truncate text-base font-semibold tracking-tight text-text">
              {pageTitle}
            </h1>
          </div>
        </div>

        <div className="hidden min-w-0 lg:block">
          <p className="text-label">KrishiSaathi</p>
          <h1 className="mt-0.5 text-lg font-semibold tracking-tight text-text">
            {pageTitle}
          </h1>
        </div>

        <div className="flex shrink-0 items-center gap-1">
          <button
            type="button"
            className="touch-target relative flex items-center justify-center rounded-lg text-text-muted transition-colors hover:bg-surface-muted hover:text-text"
            aria-label="Notifications"
          >
            <Bell className="h-[1.125rem] w-[1.125rem]" aria-hidden="true" />
            <span
              className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-attention ring-2 ring-surface"
              aria-hidden="true"
            />
          </button>
        </div>
      </div>
    </header>
  )
}

export function BottomNav() {
  const mobileNavItems = mainNavItems.filter((item) =>
    ['/', '/farm', '/health', '/market', '/saathi', '/profile'].includes(item.path),
  )

  return (
    <nav
      className="fixed inset-x-0 bottom-0 z-40 border-t border-border bg-surface lg:hidden"
      aria-label="Mobile navigation"
    >
      <ul className="mx-auto flex max-w-lg items-stretch px-0 pb-[max(0.25rem,env(safe-area-inset-bottom))]">
        {mobileNavItems.map(({ label, path, icon: Icon }) => (
          <li key={path} className="min-w-0 flex-1">
            <NavLink
              to={path}
              end={path === '/'}
              className={({ isActive }) =>
                cn(
                  'flex min-h-[3rem] flex-col items-center justify-center gap-0.5 px-0.5 py-1',
                  'text-[10px] font-medium leading-none transition-colors duration-150',
                  'touch-manipulation',
                  isActive ? 'text-forest' : 'text-text-subtle',
                )
              }
            >
              {({ isActive }) => (
                <>
                  <span
                    className={cn(
                      'flex h-7 w-7 items-center justify-center rounded-lg transition-all duration-150',
                      isActive
                        ? 'bg-primary-50 text-forest shadow-xs ring-1 ring-primary-200/60'
                        : 'text-text-muted',
                    )}
                  >
                    <Icon className="h-[1.125rem] w-[1.125rem]" aria-hidden="true" />
                  </span>
                  <span className="max-w-full truncate px-0.5">
                    {mobileLabels[path] ?? label}
                  </span>
                </>
              )}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}
