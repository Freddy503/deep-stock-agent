'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  getDashboardSummary,
  getAllLatestDecisions,
  runAnalysisNow,
  type Decision,
  type DashboardSummary,
} from '@/lib/api'
import {
  formatCurrency,
  formatPercent,
  getActionColor,
  formatDate,
  getChangeColor,
} from '@/lib/utils'
import Link from 'next/link'

export default function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [decisions, setDecisions] = useState<Decision[]>([])
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [summaryData, decisionsData] = await Promise.all([
        getDashboardSummary(),
        getAllLatestDecisions(),
      ])
      setSummary(summaryData)
      setDecisions(decisionsData)
    } catch (error) {
      console.error('Failed to load dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRunAnalysis = async () => {
    try {
      setAnalyzing(true)
      await runAnalysisNow()
      // Reload data after analysis
      setTimeout(() => {
        loadData()
      }, 2000)
    } catch (error) {
      console.error('Failed to run analysis:', error)
    } finally {
      setAnalyzing(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground mt-1">
            AI-powered portfolio insights and recommendations
          </p>
        </div>
        <Button
          onClick={handleRunAnalysis}
          disabled={analyzing}
          size="lg"
        >
          {analyzing ? 'Analyzing...' : '🤖 Run Analysis Now'}
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Portfolio Value
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(summary?.portfolio_value || 0)}
            </div>
            <p className={`text-xs mt-1 ${getChangeColor(summary?.portfolio_change_pct || 0)}`}>
              {summary?.portfolio_change_pct !== undefined && summary.portfolio_change_pct >= 0 ? '+' : ''}
              {formatPercent((summary?.portfolio_change_pct || 0) / 100)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Holdings
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {summary?.total_holdings || 0}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {summary?.total_watchlist || 0} in watchlist
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              AI Accuracy (7d)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {summary?.ai_accuracy_7d
                ? formatPercent(summary.ai_accuracy_7d)
                : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Recent predictions
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              AI Accuracy (30d)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {summary?.ai_accuracy_30d
                ? formatPercent(summary.ai_accuracy_30d)
                : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Last month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Latest Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle>Latest AI Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          {decisions.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">
                No recommendations yet. Click "Run Analysis Now" to get started.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {decisions.slice(0, 10).map((decision) => (
                <Link
                  key={decision.id}
                  href={`/stocks/${decision.symbol}`}
                  className="block"
                >
                  <div className="flex items-center justify-between p-4 rounded-lg border hover:bg-accent/50 transition-colors">
                    <div className="flex items-center gap-4">
                      <div>
                        <div className="font-semibold text-lg">
                          {decision.symbol}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {formatDate(decision.decision_date)}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-6">
                      <div className="text-right">
                        <div className="text-sm text-muted-foreground">
                          Confidence
                        </div>
                        <div className="font-medium">
                          {formatPercent(decision.confidence)}
                        </div>
                      </div>

                      <div className="text-right">
                        <div className="text-sm text-muted-foreground">
                          Risk
                        </div>
                        <div className="font-medium">
                          {formatPercent(decision.risk_score)}
                        </div>
                      </div>

                      <Badge
                        variant={
                          decision.action === 'BUY'
                            ? 'buy'
                            : decision.action === 'SELL'
                            ? 'sell'
                            : 'hold'
                        }
                        className="min-w-[60px] justify-center"
                      >
                        {decision.action}
                      </Badge>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
