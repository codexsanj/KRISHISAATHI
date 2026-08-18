import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Check, Sprout } from 'lucide-react'
import { Button, Input } from '../../components/common'
import { BrandMark } from '../../components/common/BrandMark'
import { useApp } from '../../stores/AppProvider'
import { cn } from '../../utils/cn'

const STEPS = [
  { id: 'about', label: 'About you' },
  { id: 'farm', label: 'Your farm' },
  { id: 'crop', label: 'Your crop' },
  { id: 'soil', label: 'Soil & water' },
  { id: 'location', label: 'Location' },
  { id: 'done', label: 'Done' },
]

export function OnboardingPage() {
  const navigate = useNavigate()
  const { completeOnboarding } = useApp()
  const [step, setStep] = useState(0)
  const [form, setForm] = useState({
    name: '',
    phone: '',
    farmName: '',
    area: '',
    crop: '',
    soil: '',
    waterSource: '',
    location: '',
  })

  const update = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleNext = () => {
    if (step < STEPS.length - 1) setStep((s) => s + 1)
  }

  const handleBack = () => {
    if (step > 0) setStep((s) => s - 1)
  }

  const handleFinish = () => {
    completeOnboarding({
      farmer: { name: form.name, phone: form.phone },
      farm: {
        name: form.farmName,
        crop: form.crop,
        area: form.area,
        location: form.location,
        soil: form.soil,
        waterSource: form.waterSource,
        status: 'Healthy',
      },
    })
    navigate('/')
  }

  const progress = ((step + 1) / STEPS.length) * 100

  return (
    <div className="auth-shell flex min-h-dvh flex-col">
      <header className="border-b border-border bg-surface/80 px-5 py-4 backdrop-blur-sm">
        <BrandMark size="md" />
      </header>

      <main className="mx-auto w-full max-w-lg flex-1 px-5 py-6 sm:py-8">
        {/* Progress */}
        <div className="mb-6 space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="font-medium text-forest">
              Step {step + 1} of {STEPS.length}
            </span>
            <span className="text-text-subtle">{STEPS[step].label}</span>
          </div>
          <div className="h-1.5 overflow-hidden rounded-full bg-sage-bg">
            <div
              className="h-full rounded-full bg-forest transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <div className="surface-card p-5 sm:p-6">
          {step === 0 && (
            <div className="space-y-4">
              <h2 className="text-heading-section">About you</h2>
              <p className="text-body">Tell us a little about yourself</p>
              <Input label="Your name" placeholder="Enter your name" value={form.name} onChange={update('name')} />
              <Input label="Phone number" placeholder="+91 XXXXX XXXXX" value={form.phone} onChange={update('phone')} />
            </div>
          )}

          {step === 1 && (
            <div className="space-y-4">
              <h2 className="text-heading-section">Your farm</h2>
              <p className="text-body">Basic details about your farm</p>
              <Input label="Farm name" placeholder="e.g. Green Valley Farm" value={form.farmName} onChange={update('farmName')} />
              <Input label="Farm area" placeholder="e.g. 2.5 acres" value={form.area} onChange={update('area')} />
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <h2 className="text-heading-section">Your crop</h2>
              <p className="text-body">What are you currently growing?</p>
              <Input label="Primary crop" placeholder="e.g. Wheat, Cotton, Rice" value={form.crop} onChange={update('crop')} />
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4">
              <h2 className="text-heading-section">Soil & water</h2>
              <p className="text-body">Help us understand your farm conditions</p>
              <Input label="Soil type" placeholder="e.g. Loamy, Clay, Sandy" value={form.soil} onChange={update('soil')} />
              <Input label="Water source" placeholder="e.g. Canal, Borewell, Rain-fed" value={form.waterSource} onChange={update('waterSource')} />
            </div>
          )}

          {step === 4 && (
            <div className="space-y-4">
              <h2 className="text-heading-section">Location</h2>
              <p className="text-body">Where is your farm located?</p>
              <Input label="Village / District / State" placeholder="e.g. Pune, Maharashtra" value={form.location} onChange={update('location')} />
            </div>
          )}

          {step === 5 && (
            <div className="flex flex-col items-center py-4 text-center">
              <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-sage-bg text-forest ring-1 ring-sage/30">
                <Check className="h-7 w-7" aria-hidden="true" />
              </div>
              <h2 className="text-heading-section">You&apos;re all set!</h2>
              <p className="mt-2 text-body">
                Saathi will use your farm profile to personalize recommendations.
              </p>
              <div className="mt-4 flex items-center gap-2 rounded-lg bg-sage-bg/60 px-4 py-3 text-sm text-forest">
                <Sprout className="h-4 w-4" aria-hidden="true" />
                <span>
                  {form.crop || 'Your crop'} · {form.area || 'Your farm'} · {form.location || 'Your location'}
                </span>
              </div>
            </div>
          )}
        </div>

        <div className={cn('mt-5 flex gap-3', step === 0 ? 'justify-end' : 'justify-between')}>
          {step > 0 && step < STEPS.length - 1 && (
            <Button variant="outline" onClick={handleBack}>
              Back
            </Button>
          )}
          {step < STEPS.length - 2 && (
            <Button onClick={handleNext} className="ml-auto">
              Continue
            </Button>
          )}
          {step === STEPS.length - 2 && (
            <Button onClick={handleNext} className="ml-auto">
              Review
            </Button>
          )}
          {step === STEPS.length - 1 && (
            <Button onClick={handleFinish} className="w-full" size="lg">
              Go to my farm dashboard
            </Button>
          )}
        </div>
      </main>
    </div>
  )
}
