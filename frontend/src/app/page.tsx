'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { apiService, Site } from '@/lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { BarChart3, Plus, Globe, TrendingUp, Users, Activity, LogOut } from 'lucide-react'

export default function Dashboard() {
  const router = useRouter()
  const [sites, setSites] = useState<Site[]>([])
  const [loading, setLoading] = useState(true)
  const [showNewSite, setShowNewSite] = useState(false)
  const [newSiteName, setNewSiteName] = useState('')
  const [newSiteDomain, setNewSiteDomain] = useState('')
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (!token || !userData) {
      router.push('/login')
      return
    }
    
    // Initialize auth token in axios
    apiService.setAuthToken(token)
    setUser(JSON.parse(userData))
    loadSites()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  const loadSites = async () => {
    try {
      const data = await apiService.getSites()
      setSites(data)
    } catch (error) {
      console.error('Failed to load sites:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateSite = async () => {
    try {
      const newSite = await apiService.createSite({
        name: newSiteName,
        domain: newSiteDomain
      })
      setShowNewSite(false)
      setNewSiteName('')
      setNewSiteDomain('')
      loadSites()
      alert('Site created successfully!')
    } catch (error) {
      console.error('Failed to create site:', error)
      alert('Failed to create site. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="border-b bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <TrendingUp className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold">OpenSite Analytics</h1>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-600">{user?.email}</span>
              <Button variant="outline" size="icon" onClick={handleLogout}>
                <LogOut className="h-4 w-4" />
              </Button>
              <Button onClick={() => setShowNewSite(true)}>
                <Plus className="h-4 w-4 mr-2" />
                New Site
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* New Site Form */}
        {showNewSite && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Add New Site</CardTitle>
              <CardDescription>Register a new website for analytics tracking</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateSite} className="flex gap-4">
                <Input
                  placeholder="Site Name"
                  value={newSiteName}
                  onChange={(e) => setNewSiteName(e.target.value)}
                  required
                />
                <Input
                  placeholder="example.com"
                  value={newSiteDomain}
                  onChange={(e) => setNewSiteDomain(e.target.value)}
                  required
                />
                <Button type="submit">Create Site</Button>
                <Button type="button" variant="outline" onClick={() => setShowNewSite(false)}>
                  Cancel
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Sites Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-slate-600">Loading sites...</p>
          </div>
        ) : sites.length === 0 ? (
          <Card className="text-center py-12">
            <CardContent>
              <Globe className="h-16 w-16 mx-auto text-slate-400 mb-4" />
              <h3 className="text-xl font-semibold mb-2">No sites yet</h3>
              <p className="text-slate-600 mb-4">Add your first website to start tracking analytics</p>
              <Button onClick={() => setShowNewSite(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Your First Site
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sites.map((site) => (
              <Card key={site.id} className="hover:shadow-lg transition-shadow cursor-pointer h-full" onClick={() => router.push(`/site/${site.id}`)}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg">{site.name}</CardTitle>
                      <CardDescription className="mt-1">{site.domain}</CardDescription>
                    </div>
                    <Globe className="h-5 w-5 text-slate-400" />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Status</span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        site.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {site.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Site Key</span>
                      <span className="font-mono text-xs bg-slate-100 px-2 py-1 rounded">
                        {site.site_key.slice(0, 8)}...
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
