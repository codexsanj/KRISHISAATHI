import { SectionHeader, Alert } from '../components/common'
import { SaathiChat } from '../components/saathi/SaathiChat'

export function SaathiPage() {
  return (
    <div className="space-y-4 sm:space-y-5">
      <SectionHeader
        eyebrow="Saathi"
        title="Your farming companion"
        subtitle="Ask about your crop, weather, irrigation, market, and today's tasks."
        compact
      />

      <SaathiChat />

      <Alert variant="info" title="Demo mode">
        Saathi responses are mock/demo only. Real AI with farm context integration coming soon.
      </Alert>
    </div>
  )
}
