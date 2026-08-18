import { Sprout, Leaf, CloudSun, Droplets } from 'lucide-react'
import { BrandMark } from '../common/BrandMark'

export function AuthVisualPanel() {
  return (
    <div className="relative flex h-full flex-col justify-between overflow-hidden p-8 lg:p-10 xl:p-12">
      {/* Organic decorative shapes */}
      <div className="auth-orb auth-orb-1" aria-hidden="true" />
      <div className="auth-orb auth-orb-2" aria-hidden="true" />
      <div className="auth-orb auth-orb-3" aria-hidden="true" />

      <div className="relative z-10">
        <BrandMark size="lg" inverted className="text-text-inverse" />
      </div>

      <div className="relative z-10 space-y-6">
        <div>
          <h2 className="text-2xl font-bold leading-tight tracking-tight text-text-inverse lg:text-3xl">
            Your intelligent
            <br />
            farming companion
          </h2>
          <p className="mt-3 max-w-sm text-sm leading-relaxed text-sage-light/90 lg:text-base">
            Data → Intelligence → Decision → Action.
            Know what to do, when to do it, and why.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          {[
            { icon: Sprout, label: 'Crop advisory' },
            { icon: CloudSun, label: 'Weather intel' },
            { icon: Droplets, label: 'Irrigation' },
            { icon: Leaf, label: 'Crop health' },
          ].map(({ icon: Icon, label }) => (
            <div
              key={label}
              className="flex items-center gap-2.5 rounded-lg bg-white/10 px-3 py-2.5 ring-1 ring-white/15 backdrop-blur-sm"
            >
              <Icon className="h-4 w-4 shrink-0 text-sage-light" aria-hidden="true" />
              <span className="text-xs font-medium text-text-inverse/90">{label}</span>
            </div>
          ))}
        </div>
      </div>

      <p className="relative z-10 text-xs text-sage-light/70">
        Smart India Hackathon · Agri-tech for every farmer
      </p>
    </div>
  )
}
