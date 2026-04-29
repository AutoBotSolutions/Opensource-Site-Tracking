'use client'

import { useState, useEffect, useRef } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { apiService, Site, AnalyticsData } from '@/lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Select } from '@/components/ui/select'
import { ArrowLeft, TrendingUp, Users, Activity, Clock, MousePointer, Globe, Monitor, Wifi, WifiOff } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

export default function SiteAnalytics() {
  const params = useParams()
  const router = useRouter()
  const siteId = parseInt(params.id as string)
  
  const [site, setSite] = useState<Site | null>(null)
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [period, setPeriod] = useState('7days')
  const [isConnected, setIsConnected] = useState(false)
  const [livePageviews, setLivePageviews] = useState<any[]>([])
  const [liveEvents, setLiveEvents] = useState<any[]>([])
  const [goals, setGoals] = useState<any[]>([])
  const [showGoalModal, setShowGoalModal] = useState(false)
  const [newGoalName, setNewGoalName] = useState('')
  const [newGoalType, setNewGoalType] = useState('pageview')
  const [newGoalTarget, setNewGoalTarget] = useState('')

  useEffect(() => {
    // Initialize auth token from localStorage
    const token = localStorage.getItem('token')
    if (token) {
      apiService.setAuthToken(token)
    }
    loadData()
  }, [siteId, period])

  useEffect(() => {
    // WebSocket functionality disabled for now
    if (site) {
      setIsConnected(false)
    }
  }, [site, siteId])

  const handleCreateGoal = async () => {
    try {
      await apiService.createGoal({
        site_id: siteId,
        name: newGoalName,
        goal_type: newGoalType,
        target_value: newGoalTarget || undefined
      })
      setShowGoalModal(false)
      setNewGoalName('')
      setNewGoalType('pageview')
      setNewGoalTarget('')
      loadData()
    } catch (error) {
      console.error('Failed to create goal:', error)
    }
  }

  const loadData = async () => {
    try {
      setLoading(true)
      console.log('Loading data for site:', siteId)
      const token = localStorage.getItem('token')
      console.log('Token from localStorage:', token ? 'exists' : 'missing')
      apiService.setAuthToken(token || '')
      const [siteData, analyticsData, goalsData] = await Promise.all([
        apiService.getSite(siteId),
        apiService.getAnalytics(siteId, period),
        apiService.getGoals(siteId)
      ])
      setSite(siteData)
      setAnalytics(analyticsData)
      setGoals(goalsData)
    } catch (error: any) {
      console.error('Failed to load data:', error)
      console.error('Error response:', error.response)
      if (error.response?.status === 404) {
        alert('Site not found. You may not have access to this site.')
        router.push('/')
      } else if (error.response?.status === 401) {
        alert('Session expired. Please login again.')
        router.push('/login')
      } else {
        alert(`Error loading site: ${error.message || 'Unknown error'}`)
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!site || !analytics) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Site not found</p>
      </div>
    )
  }

  const summary = analytics.summary

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="border-b bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => router.push('/')}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="text-2xl font-bold">{site.name}</h1>
                <p className="text-sm text-slate-600">{site.domain}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm">
                {isConnected ? (
                  <>
                    <Wifi className="h-4 w-4 text-green-600" />
                    <span className="text-green-600">Live</span>
                  </>
                ) : (
                  <>
                    <WifiOff className="h-4 w-4 text-slate-400" />
                    <span className="text-slate-400">Offline</span>
                  </>
                )}
              </div>
              <Select value={period} onChange={(e) => setPeriod(e.target.value)}>
                <option value="today">Today</option>
                <option value="yesterday">Yesterday</option>
                <option value="7days">Last 7 Days</option>
                <option value="30days">Last 30 Days</option>
                <option value="90days">Last 90 Days</option>
              </Select>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Total Pageviews</CardTitle>
              <TrendingUp className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{summary.total_pageviews.toLocaleString()}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Unique Visitors</CardTitle>
              <Users className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{summary.unique_visitors.toLocaleString()}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Total Sessions</CardTitle>
              <Activity className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{summary.total_sessions.toLocaleString()}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Avg. Session Duration</CardTitle>
              <Clock className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">
                {Math.floor(summary.avg_session_duration / 60)}m {Math.floor(summary.avg_session_duration % 60)}s
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Pageviews Over Time */}
          <Card>
            <CardHeader>
              <CardTitle>Pageviews Over Time</CardTitle>
              <CardDescription>Daily page view count</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics.pageviews_over_time}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="pageviews" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Device Breakdown */}
          <Card>
            <CardHeader>
              <CardTitle>Device Breakdown</CardTitle>
              <CardDescription>Visitors by device type</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={Object.entries(summary.device_breakdown).map(([name, value]) => ({ name, value }))}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {Object.entries(summary.device_breakdown).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Top Pages & Referrers */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Top Pages */}
          <Card>
            <CardHeader>
              <CardTitle>Top Pages</CardTitle>
              <CardDescription>Most visited pages</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {summary.top_pages.map(([url, count], index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1 min-w-0">
                      <span className="text-slate-400 text-sm w-6">{index + 1}</span>
                      <span className="truncate text-sm">{url}</span>
                    </div>
                    <span className="font-semibold text-sm">{count.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Top Referrers */}
          <Card>
            <CardHeader>
              <CardTitle>Top Referrers</CardTitle>
              <CardDescription>Traffic sources</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {summary.top_referrers.length > 0 ? (
                  summary.top_referrers.map(([referrer, count], index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center gap-3 flex-1 min-w-0">
                        <Globe className="h-4 w-4 text-slate-400" />
                        <span className="truncate text-sm">{referrer}</span>
                      </div>
                      <span className="font-semibold text-sm">{count.toLocaleString()}</span>
                    </div>
                  ))
                ) : (
                  <p className="text-slate-500 text-sm">No referrer data available</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Browser & Country Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Browser Breakdown */}
          <Card>
            <CardHeader>
              <CardTitle>Browser Breakdown</CardTitle>
              <CardDescription>Visitors by browser</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(summary.browser_breakdown).map(([browser, count]) => (
                  <div key={browser} className="flex items-center justify-between">
                    <span className="text-sm">{browser}</span>
                    <span className="font-semibold text-sm">{count.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Country Breakdown */}
          <Card>
            <CardHeader>
              <CardTitle>Country Breakdown</CardTitle>
              <CardDescription>Visitors by country</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(summary.country_breakdown).map(([country, count]) => (
                  <div key={country} className="flex items-center justify-between">
                    <span className="text-sm">{country}</span>
                    <span className="font-semibold text-sm">{count.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Events Summary */}
        {analytics.events_summary.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Custom Events</CardTitle>
              <CardDescription>Tracked custom events</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {analytics.events_summary.map(([eventName, count], index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <MousePointer className="h-4 w-4 text-slate-400" />
                      <span className="text-sm">{eventName}</span>
                    </div>
                    <span className="font-semibold text-sm">{count.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Live Activity Feed */}
        {(livePageviews.length > 0 || liveEvents.length > 0) && (
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Live Activity</CardTitle>
              <CardDescription>Real-time page views and events</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {livePageviews.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold mb-2">Recent Page Views</h4>
                    <div className="space-y-2">
                      {livePageviews.map((pv, index) => (
                        <div key={index} className="flex items-center justify-between text-sm p-2 bg-slate-50 rounded">
                          <div className="flex items-center gap-2">
                            <Globe className="h-4 w-4 text-blue-600" />
                            <span className="truncate max-w-xs">{pv.url}</span>
                          </div>
                          <div className="flex items-center gap-2 text-slate-500">
                            <span>{pv.device}</span>
                            {pv.country && <span>• {pv.country}</span>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {liveEvents.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold mb-2">Recent Events</h4>
                    <div className="space-y-2">
                      {liveEvents.map((ev, index) => (
                        <div key={index} className="flex items-center justify-between text-sm p-2 bg-slate-50 rounded">
                          <div className="flex items-center gap-2">
                            <MousePointer className="h-4 w-4 text-purple-600" />
                            <span>{ev.event_name}</span>
                            {ev.event_category && (
                              <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                                {ev.event_category}
                              </span>
                            )}
                          </div>
                          <span className="text-slate-500 text-xs">{new Date(ev.created_at).toLocaleTimeString()}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Integration Code */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Integration Code</CardTitle>
            <CardDescription>Add this to your website to start tracking</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto">
              <pre className="text-sm">
{`<script>
  (function(w,d,s,id){
    w.OpenSite=w.OpenSite||function(){(w.OpenSite.q=w.OpenSite.q||[]).push(arguments)};
    var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s);
    j.async=true;
    j.src='${process.env.NEXT_PUBLIC_API_URL}/tracking-script.js';
    j.id=id;
    f.parentNode.insertBefore(j,f);
  })(window,document,'script','opensite-analytics');
  
  OpenSite('init', '${site.site_key}', '${site.api_key}');
  OpenSite('trackPageview');
</script>`}
              </pre>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
