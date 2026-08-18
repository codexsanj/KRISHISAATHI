import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AppLayout } from './layouts/AppLayout'
import { AuthLayout } from './layouts/AuthLayout'
import { ProtectedRoute, GuestRoute } from './components/routing/ProtectedRoute'
import { HomePage } from './pages/HomePage'
import { FarmPage } from './pages/FarmPage'
import { HealthPage } from './pages/HealthPage'
import { MarketPage } from './pages/MarketPage'
import { SaathiPage } from './pages/SaathiPage'
import { ProfilePage } from './pages/ProfilePage'
import { LoginPage } from './pages/auth/LoginPage'
import { RegisterPage } from './pages/auth/RegisterPage'
import { OnboardingPage } from './pages/onboarding/OnboardingPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Auth routes */}
        <Route
          element={
            <GuestRoute>
              <AuthLayout />
            </GuestRoute>
          }
        >
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegisterPage />} />
        </Route>

        {/* Onboarding */}
        <Route
          path="onboarding"
          element={
            <ProtectedRoute>
              <OnboardingPage />
            </ProtectedRoute>
          }
        />

        {/* Main app */}
        <Route
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<HomePage />} />
          <Route path="farm" element={<FarmPage />} />
          <Route path="health" element={<HealthPage />} />
          <Route path="market" element={<MarketPage />} />
          <Route path="saathi" element={<SaathiPage />} />
          <Route path="profile" element={<ProfilePage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
