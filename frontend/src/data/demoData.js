/** Demo / mock data — replace with API responses later */

export const DEMO_PRIORITY_ACTION = {
  iconLabel: 'Pest risk',
  title: 'Apply neem spray to cotton field',
  dueLabel: 'Due by 4 PM',
  what: 'Spray neem oil solution on affected leaves in the north field.',
  when: 'Today before 4 PM — avoid midday heat for best absorption.',
  why: 'Early pest signs detected on cotton leaves; treatment now prevents spread to adjacent crops.',
}

export const DEMO_FARM_SNAPSHOT = {
  weather: {
    value: '32°C',
    label: 'Partly cloudy',
    detail: 'Rain likely tomorrow',
  },
  irrigation: {
    value: 'Due',
    label: 'North field',
    detail: 'Rain expected tomorrow',
  },
  cropHealth: {
    value: 'Healthy',
    label: '2 of 3 fields',
    detail: 'No major issues',
  },
  market: {
    value: 'Wheat',
    label: '+4.2%',
    detail: 'Nearby mandi prices',
  },
}

export const DEMO_ALERTS = [
  {
    id: '1',
    type: 'weather',
    title: 'Rain advisory',
    description: 'Light showers expected tomorrow — delay fertilizer application.',
  },
  {
    id: '2',
    type: 'pest',
    title: 'Pest activity rising',
    description: 'Regional cotton pest risk is moderate this week.',
  },
]

export const DEMO_FARM = {
  name: 'Green Valley Farm',
  crop: 'Wheat',
  area: '2.5 acres',
  location: 'Bengaluru, Karnataka',
  soil: 'Loamy',
  waterSource: 'Canal irrigation',
  status: 'Healthy',
}

export const DEMO_FARMER = {
  name: 'Demo Farmer',
  phone: '+91 98765 43210',
  email: 'demo@krishisaathi.app',
}

export const SAATHI_SUGGESTED_PROMPTS = [
  'Should I irrigate today?',
  'Why is my crop at risk?',
  'What should I do today?',
  'Is it a good time to sell?',
  'Check my crop health',
]

/** Mock Saathi responses — clearly demo, not real AI */
export const SAATHI_MOCK_RESPONSES = {
  'should i irrigate today?': {
    what: 'Hold irrigation for the north field today.',
    when: 'Reassess tomorrow morning after checking soil moisture.',
    why: 'Rain is likely tomorrow (60% chance). Your canal-fed north field retains moisture well — over-irrigation now could waterlog the roots.',
  },
  'why is my crop at risk?': {
    what: 'Monitor cotton leaves in the north field for pest damage.',
    when: 'Inspect today and apply neem spray before 4 PM if signs persist.',
    why: 'Early pest activity was detected in your region. Your wheat fields are healthy, but cotton in the north field shows early warning signs.',
  },
  'what should i do today?': {
    what: 'Apply neem spray to the cotton field in the north section.',
    when: 'Complete before 4 PM today.',
    why: 'This is your highest-priority action based on pest risk, weather window, and crop stage.',
  },
  'is it a good time to sell?': {
    what: 'Consider selling wheat within this week.',
    when: 'Monitor mandi prices daily — current trend is +4.2%.',
    why: 'Nearby mandi prices for wheat are rising. Holding beyond two weeks may not yield significantly better returns based on current trends.',
  },
  'check my crop health': {
    what: 'Your farm is mostly healthy — 2 of 3 fields show no issues.',
    when: 'Upload a photo of the cotton field leaves for a detailed check.',
    why: 'Wheat and the south field are healthy. The north cotton field needs attention due to early pest signs.',
  },
}

export const SAATHI_DEFAULT_RESPONSE = {
  what: 'I can help with crop, weather, irrigation, and market questions.',
  when: 'Try one of the suggested prompts for a contextual demo answer.',
  why: 'Saathi uses your farm profile, crop, weather, and soil data to give personalized guidance. This is a demo response — real AI integration coming soon.',
}

export function getSaathiMockResponse(message, farm) {
  const key = message.toLowerCase().trim()
  const matched = SAATHI_MOCK_RESPONSES[key]
  if (matched) return matched

  for (const [prompt, response] of Object.entries(SAATHI_MOCK_RESPONSES)) {
    if (key.includes(prompt.split(' ')[0]) || prompt.includes(key.slice(0, 10))) {
      return response
    }
  }

  return {
    ...SAATHI_DEFAULT_RESPONSE,
    why: `Based on your ${farm?.crop ?? 'crop'} farm in ${farm?.location ?? 'your area'}, I'd need more context. ${SAATHI_DEFAULT_RESPONSE.why}`,
  }
}
