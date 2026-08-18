import { TrendingUp } from 'lucide-react'
import { SectionHeader, EmptyState, StatCard } from '../components/common'
import { MarketCard } from '../components/common/cards'

export function MarketPage() {
  return (
    <div className="space-y-6 sm:space-y-8">
      <SectionHeader
        eyebrow="Market"
        title="Market"
        subtitle="Mandi prices, trends, and market intelligence to help you sell better."
      />

      <div className="grid gap-3 sm:grid-cols-2">
        <MarketCard
          crop="Cotton (local mandi)"
          price="₹6,420"
          description="Per quintal · updated today"
          trend={{ positive: true, label: '↑ 3.2% from last week' }}
        />
        <StatCard
          label="Best time to sell"
          value="This week"
          hint="Based on price trends"
          accent="market"
          icon={TrendingUp}
        />
      </div>

      <EmptyState
        icon={TrendingUp}
        title="Market intelligence coming soon"
        description="Track mandi prices, compare trends, and get alerts on the best time to sell your produce."
      />
    </div>
  )
}
