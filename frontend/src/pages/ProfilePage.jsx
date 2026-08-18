import { User, Bell, Droplets, Languages, LogOut } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { SectionHeader, EmptyState, Card, CardBody, Input, Button } from '../components/common'
import { AdvisoryCard } from '../components/common/cards'
import { useApp } from '../stores/AppProvider'

const features = [
  { name: 'Farmer Profile + Farm Memory', icon: User, badge: 'neutral' },
  { name: 'Multilingual + Voice', icon: Languages, badge: 'ai' },
  { name: 'Personalized Smart Alerts', icon: Bell, badge: 'attention' },
  { name: 'Intelligent Irrigation Advisory', icon: Droplets, badge: 'info' },
]

export function ProfilePage() {
  const { farmer, farm, logout } = useApp()
  const navigate = useNavigate()
  const hasProfile = Boolean(farmer?.name)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="space-y-6 sm:space-y-8">
      <SectionHeader
        eyebrow="Account"
        title="Profile"
        subtitle="Your account, language preferences, alerts, and farm settings."
        action={
          <Button variant="outline" size="sm" leftIcon={LogOut} onClick={handleLogout}>
            Sign out
          </Button>
        }
      />

      {!hasProfile ? (
        <EmptyState
          icon={User}
          title="No profile data yet"
          description="Complete onboarding to set up your farmer profile and farm memory."
        />
      ) : (
        <Card>
          <CardBody className="space-y-4">
            <p className="text-label">Your profile</p>
            <div className="grid gap-4 sm:grid-cols-2">
              <Input label="Full name" value={farmer.name ?? ''} disabled />
              <Input label="Phone" value={farmer.phone ?? ''} disabled />
            </div>
            {farm && (
              <Input
                label="Farm"
                value={[farm.crop, farm.area, farm.location].filter(Boolean).join(' · ')}
                disabled
              />
            )}
          </CardBody>
        </Card>
      )}

      <section className="space-y-3">
        <p className="text-label">Settings & features</p>
        <div className="grid gap-3 sm:grid-cols-2">
          {features.map(({ name, icon: Icon, badge }) => (
            <AdvisoryCard
              key={name}
              icon={Icon}
              badge="Soon"
              badgeVariant={badge}
              title={name}
              description="Feature preview — coming in a future release."
            />
          ))}
        </div>
      </section>
    </div>
  )
}
