import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { cn } from '@/lib/utils'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'TradingAgents Portfolio Monitor',
  description: 'AI-powered stock recommendations and portfolio monitoring',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={cn(inter.className, 'min-h-screen bg-background')}>
        <div className="flex min-h-screen">
          {/* Sidebar */}
          <aside className="w-64 border-r bg-card/50 backdrop-blur">
            <div className="flex h-full flex-col px-4 py-6">
              <div className="mb-8">
                <Link href="/">
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
                    TradingAgents
                  </h1>
                  <p className="text-xs text-muted-foreground mt-1">
                    Portfolio Monitor
                  </p>
                </Link>
              </div>

              <nav className="space-y-2">
                <Link
                  href="/"
                  className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium hover:bg-accent transition-colors"
                >
                  <span>📊</span>
                  Dashboard
                </Link>
                <Link
                  href="/portfolio"
                  className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium hover:bg-accent transition-colors"
                >
                  <span>💼</span>
                  Portfolio
                </Link>
                <Link
                  href="/analytics"
                  className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium hover:bg-accent transition-colors"
                >
                  <span>📈</span>
                  Analytics
                </Link>
              </nav>

              <div className="mt-auto pt-6 border-t">
                <div className="text-xs text-muted-foreground">
                  <p className="mb-1">Powered by</p>
                  <p className="font-semibold">TradingAgents + Gemini</p>
                </div>
              </div>
            </div>
          </aside>

          {/* Main content */}
          <main className="flex-1 overflow-auto">
            <div className="container mx-auto p-6 max-w-7xl">{children}</div>
          </main>
        </div>
      </body>
    </html>
  )
}
