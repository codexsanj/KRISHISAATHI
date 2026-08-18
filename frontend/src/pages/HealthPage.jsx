import { Leaf, Camera, Bug, Lightbulb, UserCheck } from 'lucide-react'
import { SectionHeader, EmptyState } from '../components/common'
import { RiskCard, AIRecommendationCard, AdvisoryCard } from '../components/common/cards'

const features = [
  { name: 'AI Crop Disease Detection', type: 'ai', badge: 'ai' },
  { name: 'Pest Risk Prediction', type: 'risk', badge: 'pest' },
  { name: 'Explainable Recommendations', type: 'advisory', badge: 'info' },
  { name: 'Human Expert Escalation', type: 'advisory', badge: 'neutral' },
]

export function HealthPage() {
  return (
    <div className="space-y-6 sm:space-y-8">
      <SectionHeader
        eyebrow="Health"
        title="Crop Health"
        subtitle="Disease detection, pest risk, and health alerts for your crops."
      />

      <EmptyState
        icon={Leaf}
        title="Monitor your crop health"
        description="Upload crop photos for AI disease detection, view pest risk predictions, and get explainable health advisories."
      />

      <section className="space-y-3">
        <p className="text-label">Planned features</p>
        <div className="grid gap-3 sm:grid-cols-2">
          {features.map(({ name, type, badge }) => {
            if (type === 'risk') {
              return (
                <RiskCard
                  key={name}
                  icon={Bug}
                  riskType="Pest risk"
                  title={name}
                  description="Predict and prevent pest outbreaks before they spread."
                />
              )
            }
            if (type === 'ai') {
              return (
                <AIRecommendationCard
                  key={name}
                  icon={Camera}
                  title={name}
                  description="Upload a photo to identify crop diseases with explainable results."
                />
              )
            }
            return (
              <AdvisoryCard
                key={name}
                icon={type === 'advisory' && name.includes('Expert') ? UserCheck : Lightbulb}
                badge="Soon"
                badgeVariant={badge}
                title={name}
                description="Feature preview — coming in a future release."
              />
            )
          })}
        </div>
      </section>
    </div>
  )
}
