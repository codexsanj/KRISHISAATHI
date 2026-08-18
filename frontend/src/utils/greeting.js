export function getTimeGreeting() {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 17) return 'Good afternoon'
  return 'Good evening'
}

export function getGreeting(name) {
  const greeting = getTimeGreeting()
  if (name?.trim()) return `${greeting}, ${name.trim()}`
  return greeting
}

export function getFarmContextLine(farm) {
  if (!farm) return null
  const parts = [farm.crop, farm.area, farm.location].filter(Boolean)
  return parts.length > 0 ? parts.join(' · ') : null
}
