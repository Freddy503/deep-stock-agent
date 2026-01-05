'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  getAccuracyStats,
  getAllPerformance,
  type Performance,
} from '@/lib/api'
import { formatPercent, formatNumber } from '@/lib/utils'

export default function AnalyticsPage() {
  const [stats7d, setStats7d] = useState<any>(null)
  const [stats30d, setStats30d] = useState<any>(null)
  const [performance, setPerformance] = useState<Performance[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [stats7, stats30, perfData] = await Promise.all([
        getAccuracyStats(7),
        getAccuracyStats(30),
        getAllPerformance('daily'),
      ])
      setStats7d(stats7)
      setStats30d(stats30)
      setPerformance(perfData)
    } catch (error) {
      console.error('Failed to load analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading analytics...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
        <p className="text-muted-foreground mt-1">
          AI performance metrics and accuracy tracking
        </p>
      </div>

      {/* 7-Day Stats */}
      <Card>
        <CardHeader>
          <CardTitle>7-Day Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div>
              <div className="text-sm text-muted-foreground">
                Total Predictions
              </div>
              <div className="text-2xl font-bold">
                {stats7d?.total_predictions || 0}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">
                Correct Predictions
              </div>
              <div className="text-2xl font-bold">
                {stats7d?.correct_predictions || 0}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Hit Rate</div>
              <div className="text-2xl font-bold">
                {stats7d?.hit_rate ? formatPercent(stats7d.hit_rate) : 'N/A'}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">
                Average Return
              </div>
              <div className="text-2xl font-bold">
                {stats7d?.avg_return
                  ? formatPercent(stats7d.avg_return)
                  : 'N/A'}
              </div>
            </div>
          </div>

          {stats7d?.by_action && (
            <div className="mt-6">
              <div className="text-sm font-medium mb-3">By Action</div>
              <div className="grid gap-4 md:grid-cols-3">
                {Object.entries(stats7d.by_action).map(([action, data]: [string, any]) => (
                  <div
                    key={action}
                    className="p-4 rounded-lg border bg-card/50"
                  >
                    <div className="text-sm font-medium mb-2">{action}</div>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Total:</span>
                        <span>{data.total}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Correct:</span>
                        <span>{data.correct}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">
                          Hit Rate:
                        </span>
                        <span>{formatPercent(data.hit_rate)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">
                          Avg Return:
                        </span>
                        <span>{formatPercent(data.avg_return)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* 30-Day Stats */}
      <Card>
        <CardHeader>
          <CardTitle>30-Day Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div>
              <div className="text-sm text-muted-foreground">
                Total Predictions
              </div>
              <div className="text-2xl font-bold">
                {stats30d?.total_predictions || 0}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">
                Correct Predictions
              </div>
              <div className="text-2xl font-bold">
                {stats30d?.correct_predictions || 0}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Hit Rate</div>
              <div className="text-2xl font-bold">
                {stats30d?.hit_rate ? formatPercent(stats30d.hit_rate) : 'N/A'}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">
                Average Return
              </div>
              <div className="text-2xl font-bold">
                {stats30d?.avg_return
                  ? formatPercent(stats30d.avg_return)
                  : 'N/A'}
              </div>
            </div>
          </div>

          {stats30d?.by_action && (
            <div className="mt-6">
              <div className="text-sm font-medium mb-3">By Action</div>
              <div className="grid gap-4 md:grid-cols-3">
                {Object.entries(stats30d.by_action).map(([action, data]: [string, any]) => (
                  <div
                    key={action}
                    className="p-4 rounded-lg border bg-card/50"
                  >
                    <div className="text-sm font-medium mb-2">{action}</div>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Total:</span>
                        <span>{data.total}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Correct:</span>
                        <span>{data.correct}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">
                          Hit Rate:
                        </span>
                        <span>{formatPercent(data.hit_rate)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">
                          Avg Return:
                        </span>
                        <span>{formatPercent(data.avg_return)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Recent Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Performance History</CardTitle>
        </CardHeader>
        <CardContent>
          {performance.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">
                No performance data available yet.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4">Symbol</th>
                    <th className="text-left py-3 px-4">Period</th>
                    <th className="text-left py-3 px-4">Dates</th>
                    <th className="text-left py-3 px-4">Recommendation</th>
                    <th className="text-right py-3 px-4">Actual Return</th>
                    <th className="text-right py-3 px-4">Hit</th>
                  </tr>
                </thead>
                <tbody>
                  {performance.slice(0, 20).map((perf) => (
                    <tr key={perf.id} className="border-b">
                      <td className="py-3 px-4 font-semibold">
                        {perf.symbol}
                      </td>
                      <td className="py-3 px-4">{perf.period}</td>
                      <td className="py-3 px-4 text-sm text-muted-foreground">
                        {perf.start_date} → {perf.end_date}
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={
                            perf.ai_recommendation === 'BUY'
                              ? 'text-green-500'
                              : perf.ai_recommendation === 'SELL'
                              ? 'text-red-500'
                              : 'text-gray-500'
                          }
                        >
                          {perf.ai_recommendation || 'N/A'}
                        </span>
                      </td>
                      <td className="text-right py-3 px-4">
                        {formatPercent(perf.actual_return)}
                      </td>
                      <td className="text-right py-3 px-4">
                        {perf.hit_rate > 0.5 ? '✅' : '❌'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
