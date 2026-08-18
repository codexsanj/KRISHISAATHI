import {
  Home,
  Sprout,
  Leaf,
  TrendingUp,
  MessageCircle,
  User,
} from 'lucide-react'

export const mainNavItems = [
  { label: 'Home', path: '/', icon: Home, description: 'Today\'s actions & overview' },
  { label: 'My Farm', path: '/farm', icon: Sprout, description: 'Farm profile & memory' },
  { label: 'Crop Health', path: '/health', icon: Leaf, description: 'Disease, pests & alerts' },
  { label: 'Market', path: '/market', icon: TrendingUp, description: 'Mandi prices & trends' },
  { label: 'Saathi', path: '/saathi', icon: MessageCircle, description: 'AI farming assistant' },
  { label: 'Profile', path: '/profile', icon: User, description: 'Account & preferences' },
]
