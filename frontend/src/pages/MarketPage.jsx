import { useState, useEffect } from 'react'
import { Search, MapPin, TrendingUp, AlertTriangle, ArrowLeft } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { SectionHeader, Button, Alert } from '../components/common'
import { MarketCard } from '../components/common/cards'
import { useApp } from '../stores/AppProvider'

export function MarketPage() {
  const { farm } = useApp()
  const [searchQuery, setSearchQuery] = useState('')
  const [activeCrop, setActiveCrop] = useState(null)

  const [popularCrops, setPopularCrops] = useState([])
  const [marketData, setMarketData] = useState(null)
  const [historyData, setHistoryData] = useState(null)
  const [comparisonData, setComparisonData] = useState(null)
  const [trendData, setTrendData] = useState(null)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Filters
  const [states, setStates] = useState([])
  const [selectedState, setSelectedState] = useState('')
  const [districts, setDistricts] = useState([])
  const [selectedDistrict, setSelectedDistrict] = useState('')
  const [markets, setMarkets] = useState([])
  const [selectedMarket, setSelectedMarket] = useState('')

  useEffect(() => {
    fetchInitialData()
    fetchStates()
  }, [])

  const fetchStates = async () => {
    try {
      const res = await fetch('/api/market/states')
      const data = await res.json()
      setStates(data)
    } catch (e) {
      console.error(e)
    }
  }

  const fetchDistricts = async (state) => {
    try {
      const res = await fetch(`/api/market/districts?state=${state}`)
      const data = await res.json()
      setDistricts(data)
      setSelectedDistrict('')
      setSelectedMarket('')
    } catch (e) {
      console.error(e)
    }
  }

  const fetchMarkets = async (state, district) => {
    try {
      const res = await fetch(`/api/market/markets?state=${state}&district=${district}`)
      const data = await res.json()
      setMarkets(data)
      setSelectedMarket('')
    } catch (e) {
      console.error(e)
    }
  }

  const fetchInitialData = async () => {
    setLoading(true)
    setError(null)
    try {
      const fallbackCrop = farm?.crop || 'Ginger'
      const res = await fetch(`/api/market/popular?farmer_crop=${fallbackCrop}`)
      if (!res.ok) throw new Error('Live mandi data is temporarily unavailable.')
      const data = await res.json()
      setPopularCrops(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    e?.preventDefault()
    if (!searchQuery.trim()) return
    await loadCropData(searchQuery.trim())
  }

  const loadCropData = async (crop) => {
    setLoading(true)
    setError(null)
    setActiveCrop(crop)
    try {
      let queryUrl = `/api/market/prices/current?crop=${crop}`
      if (selectedState) queryUrl += `&state=${selectedState}`
      if (selectedDistrict) queryUrl += `&district=${selectedDistrict}`
      if (selectedMarket) queryUrl += `&market=${selectedMarket}`

      const [priceRes, historyRes, compareRes, trendRes] = await Promise.all([
        fetch(queryUrl),
        fetch(`/api/market/prices/history?crop=${crop}&days=30`),
        fetch(`/api/market/compare?crop=${crop}`),
        fetch(`/api/market/trends?crop=${crop}`)
      ])

      if (!priceRes.ok) throw new Error('Live mandi data is temporarily unavailable.')

      const priceData = await priceRes.json()
      const histData = await historyRes.json()
      const compData = await compareRes.json()
      const trData = await trendRes.json()

      setMarketData(priceData.prices && priceData.prices.length > 0 ? priceData.prices[0] : null)
      setHistoryData(histData)
      setComparisonData(compData)
      setTrendData(trData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleStateChange = (e) => {
    const val = e.target.value
    setSelectedState(val)
    if (val) fetchDistricts(val)
  }

  const handleDistrictChange = (e) => {
    const val = e.target.value
    setSelectedDistrict(val)
    if (selectedState && val) fetchMarkets(selectedState, val)
  }

  const resetSearch = () => {
    setActiveCrop(null)
    setSearchQuery('')
    setMarketData(null)
    setHistoryData(null)
    setComparisonData(null)
    setTrendData(null)
    setSelectedState('')
    setSelectedDistrict('')
    setSelectedMarket('')
  }

  const formatPrice = (p) => (typeof p === 'number' ? `₹${p.toLocaleString('en-IN')}` : 'Price unavailable')

  if (loading && !activeCrop && popularCrops.length === 0) {
    return <div className="p-4 text-center text-text-subtle">Loading market intelligence...</div>
  }

  return (
    <div className="space-y-6 sm:space-y-8 pb-12">
      <SectionHeader
        eyebrow="Market"
        title="Market Intelligence"
        subtitle="Mandi prices, trends, and market comparison to help you sell better."
      />

      {/* Search & Filters */}
      <div className="rounded-xl border border-border bg-surface p-4 shadow-sm">
        <form onSubmit={handleSearch} className="flex flex-col gap-3 sm:flex-row">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-subtle" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search crop to see mandi prices..."
              className="w-full rounded-lg border border-border bg-surface px-9 py-2 text-sm focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
            />
          </div>
          <select
            value={selectedState}
            onChange={handleStateChange}
            className="rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text focus:outline-none"
          >
            <option value="">All India</option>
            {states.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
          {selectedState && (
            <select
              value={selectedDistrict}
              onChange={handleDistrictChange}
              className="rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text focus:outline-none"
            >
              <option value="">All Districts</option>
              {districts.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          )}
          {selectedDistrict && (
            <select
              value={selectedMarket}
              onChange={(e) => setSelectedMarket(e.target.value)}
              className="rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text focus:outline-none"
            >
              <option value="">All Markets</option>
              {markets.map((m) => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          )}
          <Button type="submit" variant="primary">Search</Button>
        </form>
      </div>

      {error && (
        <Alert variant="error" title="Data Error">
          {error}
        </Alert>
      )}

      {/* Default View: Popular Crops */}
      {!activeCrop && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-text">Popular / Recommended Crops</h3>
          {popularCrops.length > 0 ? (
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
              {popularCrops.map((c) => (
                <MarketCard
                  key={c.commodity}
                  crop={c.commodity}
                  price={formatPrice(c.modal_price)}
                  description={`${c.market} · ${c.date}`}
                  trend={{
                    positive: c.trend_direction === 'up',
                    label: `${c.trend_direction === 'up' ? '↑' : '↓'} ${c.trend_pct}%`,
                  }}
                  onClick={() => loadCropData(c.commodity)}
                />
              ))}
            </div>
          ) : (
            <p className="text-text-subtle">No popular crops available.</p>
          )}
        </div>
      )}

      {/* Active Crop View */}
      {activeCrop && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <button onClick={resetSearch} className="flex items-center text-sm font-medium text-forest">
              <ArrowLeft className="mr-1 h-4 w-4" /> Back to popular crops
            </button>
            <div className="text-sm text-text-subtle">
              Source: <strong>{marketData?.source || 'AGMARKNET'}</strong>
            </div>
          </div>

          {!marketData && !loading ? (
            <Alert variant="warning" title="No market data available">
              No price reported for this crop in the selected market/region.
            </Alert>
          ) : loading ? (
            <div className="py-8 text-center text-text-subtle">Loading data for {activeCrop}...</div>
          ) : (
            <>
              {/* Main Info */}
              <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                <div className="mb-4 border-b border-border pb-4">
                  <h2 className="text-2xl font-bold text-text uppercase tracking-wider">{marketData.commodity}</h2>
                  <p className="flex items-center text-sm text-text-subtle mt-1">
                    <MapPin className="mr-1 h-4 w-4" /> {marketData.market}, {marketData.district}, {marketData.state}
                  </p>
                  <p className="text-sm text-text-subtle mt-1">Date: {marketData.date}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                  <div className="rounded-lg bg-market/10 p-3">
                    <p className="text-xs font-medium text-market uppercase tracking-wide">Modal Price</p>
                    <p className="mt-1 text-xl font-semibold text-text">{formatPrice(marketData.modal_price)}</p>
                    <p className="text-xs text-text-subtle">{marketData.unit}</p>
                  </div>
                  <div className="rounded-lg bg-sage-bg p-3">
                    <p className="text-xs font-medium text-text-subtle uppercase tracking-wide">Average</p>
                    <p className="mt-1 text-xl font-semibold text-text">{formatPrice(marketData.average_price)}</p>
                    <p className="text-xs text-text-subtle">{marketData.unit}</p>
                  </div>
                  <div className="rounded-lg bg-sage-bg p-3">
                    <p className="text-xs font-medium text-text-subtle uppercase tracking-wide">Minimum</p>
                    <p className="mt-1 text-xl font-semibold text-text">{formatPrice(marketData.min_price)}</p>
                    <p className="text-xs text-text-subtle">{marketData.unit}</p>
                  </div>
                  <div className="rounded-lg bg-sage-bg p-3">
                    <p className="text-xs font-medium text-text-subtle uppercase tracking-wide">Maximum</p>
                    <p className="mt-1 text-xl font-semibold text-text">{formatPrice(marketData.max_price)}</p>
                    <p className="text-xs text-text-subtle">{marketData.unit}</p>
                  </div>
                </div>
              </div>

              {/* Chart */}
              {historyData && historyData.history && historyData.history.length > 0 ? (
                <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                  <h3 className="mb-4 text-lg font-semibold text-text">Historical Price Trend (Last 30 Days)</h3>
                  <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={historyData.history} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                        <XAxis dataKey="date" tick={{ fontSize: 12, fill: '#64748B' }} axisLine={false} tickLine={false} />
                        <YAxis tick={{ fontSize: 12, fill: '#64748B' }} axisLine={false} tickLine={false} tickFormatter={(val) => `₹${val}`} />
                        <Tooltip 
                          formatter={(value) => [`₹${value}`, 'Modal Price']}
                          labelStyle={{ color: '#0F172A', fontWeight: 'bold' }}
                          contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Line type="monotone" dataKey="modal_price" stroke="#059669" strokeWidth={3} dot={{ r: 4, fill: '#059669', strokeWidth: 2, stroke: '#FFF' }} activeDot={{ r: 6 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="mt-4 flex justify-between text-sm">
                    <span className="text-text-subtle">Lowest: <strong>{formatPrice(historyData.lowest_price)}</strong></span>
                    <span className="text-text-subtle">Highest: <strong>{formatPrice(historyData.highest_price)}</strong></span>
                    <span className="text-text-subtle">Average: <strong>{formatPrice(historyData.average_price)}</strong></span>
                  </div>
                </div>
              ) : (
                <Alert variant="warning" title="Trend Unavailable">
                  Historical data unavailable.
                </Alert>
              )}

              <div className="grid gap-6 sm:grid-cols-2">
                {/* Comparison */}
                {comparisonData && comparisonData.comparison && comparisonData.comparison.length > 0 && (
                  <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                    <h3 className="mb-4 text-lg font-semibold text-text">Nearby Markets</h3>
                    <div className="space-y-3">
                      {comparisonData.comparison.map((market, idx) => (
                        <div key={idx} className="flex items-center justify-between border-b border-border pb-2 last:border-0 last:pb-0">
                          <div>
                            <p className="font-medium text-text">{market.market}</p>
                            <p className="text-xs text-text-subtle">{market.date}</p>
                          </div>
                          <div className="text-right">
                            <p className="font-semibold text-text">{formatPrice(market.modal_price)}</p>
                            <p className={`text-xs ${market.trend_direction === 'up' ? 'text-success' : 'text-pest'}`}>
                              {market.trend_direction === 'up' ? '↑' : '↓'} {market.trend_pct}%
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Selling Intelligence */}
                {trendData && (
                  <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                    <div className="mb-4 flex items-center gap-2 text-lg font-semibold text-text">
                      <TrendingUp className="h-5 w-5 text-forest" />
                      Selling Intelligence
                    </div>
                    <div className="space-y-4 text-sm text-text">
                      <div className="rounded-lg bg-sage-bg p-3">
                        <p className="font-medium text-text">Best Available Market</p>
                        <p className="mt-1 text-forest font-semibold">{trendData.highest_market} — {formatPrice(trendData.highest_price)}</p>
                      </div>
                      <div>
                        <p className="font-medium text-text">Current Market Position</p>
                        <p className="mt-1 text-text-muted">{trendData.forecast}</p>
                      </div>
                      <div>
                        <p className="font-medium text-text">Recommendation</p>
                        <p className="mt-1 text-text-muted">{trendData.recommendation}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}
