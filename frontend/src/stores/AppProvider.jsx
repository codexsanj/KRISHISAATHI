import { createContext, useContext, useCallback, useMemo, useState, useEffect } from 'react'
import { DEMO_FARM, DEMO_FARMER } from '../data/demoData'

const STORAGE_KEY = 'krishisaathi_session'

const defaultSession = {
  isAuthenticated: false,
  onboardingComplete: false,
  farmer: null,
  farm: null,
}

function loadSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? { ...defaultSession, ...JSON.parse(raw) } : defaultSession
  } catch {
    return defaultSession
  }
}

function saveSession(session) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(session))
}

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [session, setSession] = useState(loadSession)

  useEffect(() => {
    saveSession(session)
  }, [session])

  const login = useCallback(({ phone, email }) => {
    setSession((prev) => ({
      ...prev,
      isAuthenticated: true,
      farmer: {
        name: prev.farmer?.name ?? '',
        phone: phone ?? prev.farmer?.phone ?? '',
        email: email ?? prev.farmer?.email ?? '',
      },
    }))
  }, [])

  const loginAsDemo = useCallback(() => {
    setSession({
      isAuthenticated: true,
      onboardingComplete: true,
      farmer: { ...DEMO_FARMER },
      farm: { ...DEMO_FARM },
    })
  }, [])

  const register = useCallback(({ phone, email }) => {
    setSession({
      isAuthenticated: true,
      onboardingComplete: false,
      farmer: { name: '', phone: phone ?? '', email: email ?? '' },
      farm: null,
    })
  }, [])

  const completeOnboarding = useCallback((data) => {
    setSession((prev) => ({
      ...prev,
      onboardingComplete: true,
      farmer: { ...prev.farmer, ...data.farmer },
      farm: { ...data.farm },
    }))
  }, [])

  const updateProfile = useCallback((updates) => {
    setSession((prev) => ({
      ...prev,
      farmer: { ...prev.farmer, ...updates.farmer },
      farm: prev.farm ? { ...prev.farm, ...updates.farm } : updates.farm,
    }))
  }, [])

  const logout = useCallback(() => {
    setSession(defaultSession)
    localStorage.removeItem(STORAGE_KEY)
  }, [])

  const value = useMemo(
    () => ({
      ...session,
      login,
      loginAsDemo,
      register,
      completeOnboarding,
      updateProfile,
      logout,
    }),
    [session, login, loginAsDemo, register, completeOnboarding, updateProfile, logout],
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}
