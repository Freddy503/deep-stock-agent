'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  getPortfolio,
  getWatchlist,
  addToWatchlist,
  removeFromWatchlist,
  type PortfolioHolding,
  type WatchlistStock,
} from '@/lib/api'
import {
  formatCurrency,
  formatPercent,
  formatNumber,
  getChangeColor,
} from '@/lib/utils'

export default function PortfolioPage() {
  const [holdings, setHoldings] = useState<PortfolioHolding[]>([])
  const [watchlist, setWatchlist] = useState<WatchlistStock[]>([])
  const [loading, setLoading] = useState(true)
  const [newSymbol, setNewSymbol] = useState('')
  const [adding, setAdding] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [portfolioData, watchlistData] = await Promise.all([
        getPortfolio(),
        getWatchlist(),
      ])
      setHoldings(portfolioData)
      setWatchlist(watchlistData)
    } catch (error) {
      console.error('Failed to load portfolio:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddToWatchlist = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newSymbol.trim()) return

    try {
      setAdding(true)
      await addToWatchlist(newSymbol.toUpperCase())
      setNewSymbol('')
      await loadData()
    } catch (error) {
      console.error('Failed to add to watchlist:', error)
    } finally {
      setAdding(false)
    }
  }

  const handleRemoveFromWatchlist = async (symbol: string) => {
    if (!confirm(`Remove ${symbol} from watchlist?`)) return

    try {
      await removeFromWatchlist(symbol)
      await loadData()
    } catch (error) {
      console.error('Failed to remove from watchlist:', error)
    }
  }

  // Calculate total portfolio value and P&L
  const totalValue = holdings.reduce(
    (sum, h) => sum + (h.current_value || 0),
    0
  )
  const totalCost = holdings.reduce(
    (sum, h) => sum + h.shares * h.avg_cost,
    0
  )
  const totalPnL = totalValue - totalCost
  const totalPnLPct = totalCost > 0 ? (totalPnL / totalCost) * 100 : 0

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading portfolio...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Portfolio</h1>
        <p className="text-muted-foreground mt-1">
          Manage your holdings and watchlist
        </p>
      </div>

      {/* Portfolio Summary */}
      {holdings.length > 0 && (
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total Value
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(totalValue)}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total P&L
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${getChangeColor(totalPnL)}`}>
                {totalPnL >= 0 ? '+' : ''}
                {formatCurrency(totalPnL)}
              </div>
              <p className={`text-xs mt-1 ${getChangeColor(totalPnLPct)}`}>
                {totalPnLPct >= 0 ? '+' : ''}
                {formatNumber(totalPnLPct)}%
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
              <div className="text-2xl font-bold">{holdings.length}</div>
              <p className="text-xs text-muted-foreground mt-1">
                Active positions
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Holdings Table */}
      <Card>
        <CardHeader>
          <CardTitle>Holdings</CardTitle>
        </CardHeader>
        <CardContent>
          {holdings.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">
                No holdings yet. Add stocks to your portfolio to get started.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4">Symbol</th>
                    <th className="text-right py-3 px-4">Shares</th>
                    <th className="text-right py-3 px-4">Avg Cost</th>
                    <th className="text-right py-3 px-4">Current Price</th>
                    <th className="text-right py-3 px-4">Value</th>
                    <th className="text-right py-3 px-4">P&L</th>
                    <th className="text-right py-3 px-4">P&L %</th>
                  </tr>
                </thead>
                <tbody>
                  {holdings.map((holding) => (
                    <tr key={holding.id} className="border-b">
                      <td className="py-3 px-4 font-semibold">
                        {holding.symbol}
                      </td>
                      <td className="text-right py-3 px-4">
                        {formatNumber(holding.shares, 4)}
                      </td>
                      <td className="text-right py-3 px-4">
                        {formatCurrency(holding.avg_cost)}
                      </td>
                      <td className="text-right py-3 px-4">
                        {holding.current_price
                          ? formatCurrency(holding.current_price)
                          : 'N/A'}
                      </td>
                      <td className="text-right py-3 px-4">
                        {holding.current_value
                          ? formatCurrency(holding.current_value)
                          : 'N/A'}
                      </td>
                      <td
                        className={`text-right py-3 px-4 ${
                          holding.unrealized_pnl
                            ? getChangeColor(holding.unrealized_pnl)
                            : ''
                        }`}
                      >
                        {holding.unrealized_pnl ? (
                          <>
                            {holding.unrealized_pnl >= 0 ? '+' : ''}
                            {formatCurrency(holding.unrealized_pnl)}
                          </>
                        ) : (
                          'N/A'
                        )}
                      </td>
                      <td
                        className={`text-right py-3 px-4 ${
                          holding.unrealized_pnl_pct
                            ? getChangeColor(holding.unrealized_pnl_pct)
                            : ''
                        }`}
                      >
                        {holding.unrealized_pnl_pct ? (
                          <>
                            {holding.unrealized_pnl_pct >= 0 ? '+' : ''}
                            {formatPercent(holding.unrealized_pnl_pct)}
                          </>
                        ) : (
                          'N/A'
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Watchlist */}
      <Card>
        <CardHeader>
          <CardTitle>Watchlist</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleAddToWatchlist} className="flex gap-2 mb-4">
            <input
              type="text"
              value={newSymbol}
              onChange={(e) => setNewSymbol(e.target.value)}
              placeholder="Enter symbol (e.g., AAPL)"
              className="flex-1 px-3 py-2 bg-background border rounded-md"
              disabled={adding}
            />
            <Button type="submit" disabled={adding || !newSymbol.trim()}>
              {adding ? 'Adding...' : 'Add to Watchlist'}
            </Button>
          </form>

          {watchlist.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">
                No stocks in watchlist. Add stocks above to start monitoring.
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {watchlist.map((stock) => (
                <div
                  key={stock.id}
                  className="flex items-center justify-between p-3 rounded-lg border"
                >
                  <div>
                    <div className="font-semibold">{stock.symbol}</div>
                    {stock.name && (
                      <div className="text-sm text-muted-foreground">
                        {stock.name}
                      </div>
                    )}
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleRemoveFromWatchlist(stock.symbol)}
                  >
                    Remove
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
