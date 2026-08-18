import { Outlet, Link } from 'react-router-dom'
import { AuthVisualPanel } from '../components/auth/AuthVisualPanel'
import { BrandMark } from '../components/common/BrandMark'

export function AuthLayout() {
  return (
    <div className="auth-shell flex min-h-dvh">
      {/* Desktop visual panel */}
      <div className="auth-panel hidden lg:flex lg:w-[45%] xl:w-[42%]">
        <AuthVisualPanel />
      </div>

      {/* Form area */}
      <div className="relative flex flex-1 flex-col">
        <div className="auth-orb auth-orb-mobile pointer-events-none lg:hidden" aria-hidden="true" />

        <header className="relative z-10 px-5 py-5 sm:px-8">
          <Link to="/login" className="lg:hidden">
            <BrandMark size="md" />
          </Link>
        </header>

        <main className="relative z-10 flex flex-1 items-center justify-center px-5 pb-8 sm:px-8">
          <div className="w-full max-w-sm">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
