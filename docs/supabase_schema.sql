-- TradingAgents Portfolio Monitor Database Schema
-- Execute this SQL in your Supabase SQL Editor to create all tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Watchlist table: stocks to monitor
CREATE TABLE IF NOT EXISTS watchlist (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(255),
    added_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,

    CONSTRAINT symbol_uppercase CHECK (symbol = UPPER(symbol))
);

-- Add index on symbol for faster lookups
CREATE INDEX IF NOT EXISTS idx_watchlist_symbol ON watchlist(symbol);
CREATE INDEX IF NOT EXISTS idx_watchlist_active ON watchlist(is_active) WHERE is_active = TRUE;

-- Decisions table: AI recommendations over time
CREATE TABLE IF NOT EXISTS decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(10) NOT NULL,
    decision_date DATE NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('BUY', 'SELL', 'HOLD')),
    confidence DECIMAL(5,4) CHECK (confidence >= 0 AND confidence <= 1),
    risk_score DECIMAL(5,4) CHECK (risk_score >= 0 AND risk_score <= 1),
    reasoning TEXT,
    raw_response JSONB,
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT unique_symbol_date UNIQUE(symbol, decision_date),
    CONSTRAINT symbol_uppercase CHECK (symbol = UPPER(symbol))
);

-- Indexes for decisions
CREATE INDEX IF NOT EXISTS idx_decisions_symbol ON decisions(symbol);
CREATE INDEX IF NOT EXISTS idx_decisions_date ON decisions(decision_date DESC);
CREATE INDEX IF NOT EXISTS idx_decisions_symbol_date ON decisions(symbol, decision_date DESC);
CREATE INDEX IF NOT EXISTS idx_decisions_action ON decisions(action);

-- Prices table: historical market prices
CREATE TABLE IF NOT EXISTS prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(10) NOT NULL,
    price_date DATE NOT NULL,
    open_price DECIMAL(12,4) CHECK (open_price >= 0),
    high_price DECIMAL(12,4) CHECK (high_price >= 0),
    low_price DECIMAL(12,4) CHECK (low_price >= 0),
    close_price DECIMAL(12,4) CHECK (close_price >= 0),
    volume BIGINT CHECK (volume >= 0),

    CONSTRAINT unique_price_symbol_date UNIQUE(symbol, price_date),
    CONSTRAINT symbol_uppercase CHECK (symbol = UPPER(symbol)),
    CONSTRAINT price_validation CHECK (
        low_price <= open_price AND
        low_price <= close_price AND
        high_price >= open_price AND
        high_price >= close_price
    )
);

-- Indexes for prices
CREATE INDEX IF NOT EXISTS idx_prices_symbol ON prices(symbol);
CREATE INDEX IF NOT EXISTS idx_prices_date ON prices(price_date DESC);
CREATE INDEX IF NOT EXISTS idx_prices_symbol_date ON prices(symbol, price_date DESC);

-- Portfolio table: current holdings
CREATE TABLE IF NOT EXISTS portfolio (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(10) NOT NULL UNIQUE,
    shares DECIMAL(12,4) NOT NULL CHECK (shares > 0),
    avg_cost DECIMAL(12,4) NOT NULL CHECK (avg_cost > 0),
    first_purchase DATE,
    last_updated TIMESTAMP DEFAULT NOW(),

    CONSTRAINT symbol_uppercase CHECK (symbol = UPPER(symbol))
);

-- Index for portfolio
CREATE INDEX IF NOT EXISTS idx_portfolio_symbol ON portfolio(symbol);

-- Performance table: tracking AI accuracy
CREATE TABLE IF NOT EXISTS performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(10) NOT NULL,
    period VARCHAR(20) NOT NULL CHECK (period IN ('daily', 'weekly', 'monthly')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    ai_recommendation VARCHAR(10) CHECK (ai_recommendation IN ('BUY', 'SELL', 'HOLD')),
    actual_return DECIMAL(8,4),
    hit_rate DECIMAL(5,4) CHECK (hit_rate >= 0 AND hit_rate <= 1),
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT symbol_uppercase CHECK (symbol = UPPER(symbol)),
    CONSTRAINT valid_date_range CHECK (end_date >= start_date)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_performance_symbol ON performance(symbol);
CREATE INDEX IF NOT EXISTS idx_performance_period ON performance(period);
CREATE INDEX IF NOT EXISTS idx_performance_start_date ON performance(start_date DESC);
CREATE INDEX IF NOT EXISTS idx_performance_symbol_period ON performance(symbol, period, start_date DESC);

-- Create a view for latest decisions per stock
CREATE OR REPLACE VIEW latest_decisions AS
SELECT DISTINCT ON (symbol)
    symbol,
    decision_date,
    action,
    confidence,
    risk_score,
    reasoning,
    raw_response,
    created_at
FROM decisions
ORDER BY symbol, decision_date DESC;

-- Create a view for latest prices per stock
CREATE OR REPLACE VIEW latest_prices AS
SELECT DISTINCT ON (symbol)
    symbol,
    price_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume
FROM prices
ORDER BY symbol, price_date DESC;

-- Create a view for portfolio with current values
CREATE OR REPLACE VIEW portfolio_with_values AS
SELECT
    p.id,
    p.symbol,
    p.shares,
    p.avg_cost,
    p.first_purchase,
    p.last_updated,
    pr.close_price as current_price,
    (p.shares * pr.close_price) as current_value,
    (p.shares * p.avg_cost) as cost_basis,
    ((p.shares * pr.close_price) - (p.shares * p.avg_cost)) as unrealized_pnl,
    (((p.shares * pr.close_price) - (p.shares * p.avg_cost)) / (p.shares * p.avg_cost)) * 100 as unrealized_pnl_pct
FROM portfolio p
LEFT JOIN latest_prices pr ON p.symbol = pr.symbol;

-- Comments for documentation
COMMENT ON TABLE watchlist IS 'Stocks being monitored for AI analysis';
COMMENT ON TABLE decisions IS 'AI-generated trading recommendations';
COMMENT ON TABLE prices IS 'Historical stock price data from yfinance';
COMMENT ON TABLE portfolio IS 'User portfolio holdings';
COMMENT ON TABLE performance IS 'Performance tracking of AI recommendations';

COMMENT ON COLUMN decisions.confidence IS 'AI confidence in recommendation (0-1)';
COMMENT ON COLUMN decisions.risk_score IS 'Risk assessment score (0-1, higher = more risky)';
COMMENT ON COLUMN performance.hit_rate IS 'Whether AI prediction was correct (1.0 = correct, 0.0 = incorrect)';

-- Grant permissions (adjust for your Supabase setup)
-- These are standard permissions for the anon and authenticated roles

-- For anonymous access (read-only for public data)
GRANT SELECT ON watchlist TO anon;
GRANT SELECT ON latest_decisions TO anon;
GRANT SELECT ON latest_prices TO anon;

-- For authenticated users (full access)
GRANT ALL ON watchlist TO authenticated;
GRANT ALL ON decisions TO authenticated;
GRANT ALL ON prices TO authenticated;
GRANT ALL ON portfolio TO authenticated;
GRANT ALL ON performance TO authenticated;
GRANT SELECT ON latest_decisions TO authenticated;
GRANT SELECT ON latest_prices TO authenticated;
GRANT SELECT ON portfolio_with_values TO authenticated;

-- Sample data for testing (optional)
-- Uncomment to insert sample data

-- INSERT INTO watchlist (symbol, name) VALUES
--     ('AAPL', 'Apple Inc.'),
--     ('GOOGL', 'Alphabet Inc.'),
--     ('MSFT', 'Microsoft Corporation'),
--     ('TSLA', 'Tesla Inc.'),
--     ('AMZN', 'Amazon.com Inc.');

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'TradingAgents Portfolio Monitor schema created successfully!';
    RAISE NOTICE 'Tables created: watchlist, decisions, prices, portfolio, performance';
    RAISE NOTICE 'Views created: latest_decisions, latest_prices, portfolio_with_values';
END $$;
