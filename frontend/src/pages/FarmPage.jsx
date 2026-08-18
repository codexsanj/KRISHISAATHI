import { Sprout } from 'lucide-react'
import { Link } from 'react-router-dom'
import { SectionHeader, EmptyState, Button } from '../components/common'
import { FarmSummaryCard, AIRecommendationCard, AdvisoryCard } from '../components/common/cards'
import { useApp } from '../stores/AppProvider'

const features = [
  { name: 'Smart Crop Recommendation', badge: 'ai', type: 'ai' },
  { name: 'Personalized Crop Calendar', badge: 'neutral', type: 'advisory' },
  { name: 'Farm Profit Simulator', badge: 'market', type: 'market' },
  { name: 'Farmer Profile + Farm Memory', badge: 'neutral', type: 'advisory' },
]

export function FarmPage() {
  const { farm } = useApp()
  const hasFarm = Boolean(farm?.crop || farm?.location)

  return (
    <div className="space-y-6 sm:space-y-8">
      <SectionHeader
        eyebrow="Farm"
        title="My Farm"
        subtitle="Your farm profile, crop calendar, profit simulator, and farm memory."
      />

      {hasFarm ? (
        <FarmSummaryCard
          crop={farm.crop}
          area={farm.area}
          location={farm.location}
          status={farm.status ?? 'Healthy'}
        />
      ) : (
        <EmptyState
          icon={Sprout}
          title="No farm data yet"
          description="Add your farm details and Saathi can start personalizing your recommendations."
          action={
            <Link to="/onboarding">
              <Button>Set up farm profile</Button>
            </Link>
          }
        />
      )}

      <section className="space-y-3">
        <p className="text-label">Planned features</p>
        <div className="grid gap-3 sm:grid-cols-2">
          {features.map(({ name, badge, type }) =>
            type === 'ai' ? (
              <AIRecommendationCard
                key={name}
                title={name}
                description="Personalized recommendations based on your farm data."
              />
            ) : (
              <AdvisoryCard
                key={name}
                badge="Soon"
                badgeVariant={badge}
                title={name}
                description="Feature preview — coming in a future release."
              />
            ),
          )}
        </div>
      </section>
    </div>
  )
}
