import { Navigate, useLocation } from 'react-router-dom'
import { useApp } from '../../stores/AppProvider'

export function ProtectedRoute({ children }) {
  const { isAuthenticated, onboardingComplete } = useApp()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (!onboardingComplete && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />
  }

  if (onboardingComplete && location.pathname === '/onboarding') {
    return <Navigate to="/" replace />
  }

  return children
}

export function GuestRoute({ children }) {
  const { isAuthenticated, onboardingComplete } = useApp()

  if (isAuthenticated && onboardingComplete) {
    return <Navigate to="/" replace />
  }

  if (isAuthenticated && !onboardingComplete) {
    return <Navigate to="/onboarding" replace />
  }

  return children
}
