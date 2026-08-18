import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button, Input } from '../../components/common'
import { useApp } from '../../stores/AppProvider'

export function RegisterPage() {
  const navigate = useNavigate()
  const { register } = useApp()
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const isEmail = identifier.includes('@')
    register(isEmail ? { email: identifier } : { phone: identifier })
    navigate('/onboarding')
  }

  return (
    <div className="space-y-6">
      <div className="space-y-1.5 text-center lg:text-left">
        <h1 className="text-2xl font-bold tracking-tight text-text">Create your account</h1>
        <p className="text-body">Start your journey with intelligent farm guidance</p>
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
          placeholder="Create a password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="new-password"
        />
        <Button type="submit" className="w-full" size="lg">
          Continue
        </Button>
      </form>

      <p className="text-center text-sm text-text-muted">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-forest hover:underline">
          Sign in
        </Link>
      </p>

      <p className="text-center text-xs text-text-subtle">
        Demo mode — no real authentication connected yet
      </p>
    </div>
  )
}
