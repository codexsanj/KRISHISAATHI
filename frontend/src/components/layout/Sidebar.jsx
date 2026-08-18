import { NavLink } from 'react-router-dom'
import { mainNavItems } from '../../data/navigation'
import { BrandMark } from '../common/BrandMark'
import { cn } from '../../utils/cn'

export function Sidebar() {
  return (
    <aside className="hidden lg:flex lg:w-60 xl:w-64 lg:shrink-0 lg:flex-col lg:border-r lg:border-border lg:bg-surface-sidebar">
      <div className="border-b border-border px-5 py-4">
        <BrandMark size="md" />
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4" aria-label="Main navigation">
        <ul className="space-y-0.5">
          {mainNavItems.map(({ label, path, icon: Icon, description }) => (
            <li key={path}>
              <NavLink
                to={path}
                end={path === '/'}
                className={({ isActive }) =>
                  cn(
                    'group flex items-center gap-3 rounded-lg py-2.5 pl-2.5 pr-3 text-sm font-medium',
                    'transition-all duration-150',
                    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-forest/30 focus-visible:ring-offset-2',
                    isActive
                      ? 'nav-item-active shadow-xs'
                      : 'nav-item-idle hover:bg-surface-muted hover:text-text',
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon
                      className={cn(
                        'h-[1.125rem] w-[1.125rem] shrink-0 transition-colors',
                        isActive ? 'text-forest' : 'text-text-subtle group-hover:text-forest/70',
                      )}
                      aria-hidden="true"
                    />
                    <span className="min-w-0">
                      <span className="block truncate">{label}</span>
                      <span
                        className={cn(
                          'block truncate text-xs font-normal',
                          isActive ? 'text-forest/65' : 'text-text-subtle',
                        )}
                      >
                        {description}
                      </span>
                    </span>
                  </>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="border-t border-border px-5 py-4">
        <p className="text-[11px] leading-relaxed text-text-subtle">
          Data → Intelligence → Decision → Action
        </p>
      </div>
    </aside>
  )
}
