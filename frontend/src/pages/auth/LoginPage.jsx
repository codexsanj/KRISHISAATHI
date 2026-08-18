import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button, Input } from '../../components/common'
import { useApp } from '../../stores/AppProvider'

export function LoginPage() {
  const navigate = useNavigate()
  const { login, loginAsDemo } = useApp()
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const isEmail = identifier.includes('@')
    login(isEmail ? { email: identifier } : { phone: identifier })
    navigate('/')
  }

  const handleDemo = () => {
    loginAsDemo()
    navigate('/')
  }

  return (
    <div className="space-y-6">
      <div className="space-y-1.5 text-center lg:text-left">
        <h1 className="text-2xl font-bold tracking-tight text-text">Welcome back</h1>
        <p className="text-body">Sign in to continue to your farm dashboard</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Mobile number or email"
          type="text"
          placeholder="+91 XXXXX XXXXX or you@email.com"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          autoComplete="username"
        />
        <Input
          label="Password"
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
        />
        <Button type="submit" className="w-full" size="lg">
          Continue
        </Button>
      </form>

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-border" />
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="bg-page px-2 text-text-subtle">or</span>
        </div>
      </div>

      <Button variant="secondary" className="w-full" size="lg" onClick={handleDemo}>
        Continue as demo farmer
      </Button>

      <p className="text-center text-sm text-text-muted">
        New to KrishiSaathi?{' '}
        <Link to="/register" className="font-medium text-forest hover:underline">
          Create account
        </Link>
      </p>

      <p className="text-center text-xs text-text-subtle">
        Demo mode — no real authentication connected yet
      </p>
    </div>
  )
}
