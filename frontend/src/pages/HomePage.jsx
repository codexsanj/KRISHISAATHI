import {
  CloudSun,
  Droplets,
  Leaf,
  TrendingUp,
  CheckCircle2,
  Sparkles,
  ArrowRight,
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { Alert, Button } from '../components/common'
import {
  PriorityActionCard,
  FarmSnapshotCard,
  WeatherCard,
  RiskCard,
} from '../components/common/cards'
import {
  DEMO_PRIORITY_ACTION,
  DEMO_FARM_SNAPSHOT,
  DEMO_ALERTS,
} from '../data/demoData'
import { useApp } from '../stores/AppProvider'
import { getGreeting, getFarmContextLine } from '../utils/greeting'

export function HomePage() {
  const { farmer, farm } = useApp()
  const greeting = getGreeting(farmer?.name)
  const farmLine = getFarmContextLine(farm)
  const hasFarmData = Boolean(farm?.crop || farm?.location)

  return (
    <div className="space-y-5 sm:space-y-6">
      {/* Welcome / farm context */}
      <section className="welcome-section rounded-xl border border-sage/20 bg-sage-bg/30 px-4 py-3.5 sm:px-5 sm:py-4">
        <p className="text-sm font-medium text-text-muted">{greeting}</p>
        <p className="mt-0.5 flex items-center gap-1.5 text-base font-semibold text-text">
          <CheckCircle2 className="h-4 w-4 shrink-0 text-success" aria-hidden="true" />
          {hasFarmData ? 'Your farm is looking good today' : 'Welcome to KrishiSaathi'}
        </p>
        {farmLine ? (
          <p className="mt-1 text-sm text-text-subtle">{farmLine}</p>
        ) : (
          <p className="mt-1 text-sm text-text-subtle">
            Complete your farm profile for personalized guidance
          </p>
        )}
      </section>

      {/* Main question */}
      <div>
        <p className="text-label text-forest/70">Today</p>
        <h1 className="text-heading-hero mt-0.5 sm:text-xl">
          What should I do today?
        </h1>
      </div>

      {/* Priority action */}
      <PriorityActionCard
        {...DEMO_PRIORITY_ACTION}
        onCta={() => {}}
      />

      {/* Farm snapshot */}
      <section className="space-y-3">
        <h2 className="text-heading-section">Today&apos;s farm snapshot</h2>
        <div className="grid grid-cols-2 gap-2.5 sm:gap-3 lg:grid-cols-4">
          <FarmSnapshotCard
            icon={CloudSun}
            category="Weather"
            value={DEMO_FARM_SNAPSHOT.weather.value}
            label={DEMO_FARM_SNAPSHOT.weather.label}
            detail={DEMO_FARM_SNAPSHOT.weather.detail}
            accent="weather"
          />
          <FarmSnapshotCard
            icon={Droplets}
            category="Irrigation"
            value={DEMO_FARM_SNAPSHOT.irrigation.value}
            label={DEMO_FARM_SNAPSHOT.irrigation.label}
            detail={DEMO_FARM_SNAPSHOT.irrigation.detail}
            accent="irrigation"
          />
          <FarmSnapshotCard
            icon={Leaf}
            category="Crop health"
            value={DEMO_FARM_SNAPSHOT.cropHealth.value}
            label={DEMO_FARM_SNAPSHOT.cropHealth.label}
            detail={DEMO_FARM_SNAPSHOT.cropHealth.detail}
            accent="health"
          />
          <FarmSnapshotCard
            icon={TrendingUp}
            category="Market"
            value={DEMO_FARM_SNAPSHOT.market.value}
            label={DEMO_FARM_SNAPSHOT.market.label}
            detail={DEMO_FARM_SNAPSHOT.market.detail}
            accent="market"
          />
        </div>
        <p className="text-[10px] text-text-subtle">Demo data — will connect to live sources later</p>
      </section>

      {/* Upcoming / alerts */}
      <section className="space-y-3">
        <h2 className="text-heading-section">Upcoming & alerts</h2>
        <div className="grid gap-3 md:grid-cols-2">
          {DEMO_ALERTS.map((alert) =>
            alert.type === 'weather' ? (
              <WeatherCard
                key={alert.id}
                title={alert.title}
                description={alert.description}
              />
            ) : (
              <RiskCard
                key={alert.id}
                title={alert.title}
                description={alert.description}
                level="Moderate"
              />
            ),
          )}
        </div>
      </section>

      {/* Saathi entry */}
      <section className="saathi-teaser overflow-hidden rounded-xl border border-sage/25 bg-gradient-to-br from-sage-bg/80 to-surface p-4 sm:p-5">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-3">
            <div className="saathi-glow flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-forest text-text-inverse">
              <Sparkles className="h-5 w-5" aria-hidden="true" />
            </div>
            <div>
              <p className="font-semibold text-text">Ask Saathi anything</p>
              <p className="mt-0.5 text-sm text-text-muted">
                Get answers about {farm?.crop ?? 'your crop'}, weather, irrigation & today&apos;s tasks
              </p>
            </div>
          </div>
          <Link to="/saathi" className="shrink-0">
            <Button variant="primary" rightIcon={ArrowRight}>
              Open Saathi
            </Button>
          </Link>
        </div>
      </section>

      <Alert variant="info" title="Demo mode">
        Dashboard data is mock/demo. Connect your farm profile and APIs for live recommendations.
      </Alert>
    </div>
  )
}
