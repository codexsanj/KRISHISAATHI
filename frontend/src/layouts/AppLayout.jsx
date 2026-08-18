import { Outlet } from 'react-router-dom'
import { Sidebar } from '../components/layout/Sidebar'
import { Header, BottomNav } from '../components/layout/Header'
import { FloatingSaathiButton } from '../components/saathi/FloatingSaathiButton'

export function AppLayout() {
  return (
    <div className="page-shell relative flex min-h-dvh">
      {/* Organic background orbs */}
      <div className="page-orb page-orb-1 pointer-events-none" aria-hidden="true" />
      <div className="page-orb page-orb-2 pointer-events-none" aria-hidden="true" />

      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-forest focus:px-4 focus:py-2 focus:text-text-inverse"
      >
        Skip to main content
      </a>
      <Sidebar />

      <div className="relative flex min-w-0 flex-1 flex-col">
        <Header />

        <main
          id="main-content"
          className="flex-1 overflow-x-hidden overflow-y-auto pb-[calc(3.25rem+env(safe-area-inset-bottom))] lg:pb-10"
        >
          <div className="mx-auto w-full max-w-4xl px-3 py-4 sm:px-5 sm:py-6 lg:max-w-5xl lg:px-8 lg:py-8">
            <Outlet />
          </div>
        </main>
      </div>

      <BottomNav />
      <FloatingSaathiButton />
    </div>
  )
}
