# TradingAgents Portfolio Monitor

A full-stack portfolio monitoring and AI-powered stock recommendation system built on top of the [TradingAgents](https://github.com/JosephTLucas/TradingAgents) multi-agent LLM framework, optimized for cost-effective operation with Google Gemini models.

![Dashboard](https://img.shields.io/badge/Status-Production_Ready-green)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🌟 Features

- **AI-Powered Stock Analysis**: Multi-agent system with analysts, researchers, traders, and risk managers
- **Cost-Optimized**: Uses Gemini 2.5 Flash/Flash-Lite (~$67-400/month for 30 stocks daily)
- **Portfolio Tracking**: Monitor holdings with real-time P&L calculations
- **Performance Analytics**: Track AI accuracy and prediction performance over time
- **Automated Scheduling**: Daily analysis runs after market close
- **Modern UI**: Dark-themed Next.js dashboard with real-time updates
- **Historical Tracking**: Store and analyze decision history vs. actual outcomes

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Next.js Frontend                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │  Dashboard  │  │  Portfolio  │  │  Analytics  │  │  Settings  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              TradingAgents + Gemini 2.5                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │ │
│  │  │ Analysts │  │Researchers│  │  Trader  │  │ Risk Manager │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │ │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Supabase PostgreSQL                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │
│  │  watchlist  │  │  decisions  │  │   prices    │  │ portfolio │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## 📋 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Next.js 14 + TypeScript | App Router, Server Components |
| UI | shadcn/ui + Tailwind CSS | Modern, customizable components |
| Backend | FastAPI (Python 3.11+) | High-performance API |
| Database | Supabase (PostgreSQL) | Real-time, managed database |
| LLM | Gemini 2.5 Flash/Flash-Lite | Cost-optimized AI models |
| Scheduling | APScheduler | Background job management |
| Data | yfinance + Alpha Vantage | Stock prices and fundamentals |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Supabase account (free tier)
- Google Cloud account with Gemini API access
- Alpha Vantage API key (optional, free tier)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd deep-stock-agent
```

### 2. Set Up Supabase Database

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to SQL Editor and run the schema:

```bash
cat docs/supabase_schema.sql
```

Copy the contents and execute in Supabase SQL Editor.

3. Get your credentials from Settings → API:
   - `SUPABASE_URL`
   - `SUPABASE_KEY` (anon/public key)

### 3. Set Up TradingAgents

Run the setup script to clone TradingAgents and install dependencies:

```bash
chmod +x scripts/setup_tradingagents.sh
./scripts/setup_tradingagents.sh
```

This will:
- Clone the TradingAgents repository
- Create a Python virtual environment
- Install all backend dependencies

### 4. Configure Backend

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your API keys:

```env
GOOGLE_API_KEY=your_gemini_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

### 5. Configure Frontend

```bash
cd ../frontend
cp .env.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 6. Start the Application

#### Option A: Using Docker (Recommended)

```bash
# From project root
docker-compose up -d
```

Access the app at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

#### Option B: Manual Start

**Backend:**
```bash
cd backend
source ../venv/bin/activate  # Activate virtual environment
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📖 Usage Guide

### Adding Stocks to Watchlist

1. Navigate to **Portfolio** page
2. Enter stock symbol (e.g., `AAPL`) in the watchlist form
3. Click "Add to Watchlist"

### Running AI Analysis

**Manual:**
- Click "🤖 Run Analysis Now" on the Dashboard

**Automated:**
```bash
# Configure schedule via API or UI
curl -X POST "http://localhost:8000/api/schedule/start?hour=18&minute=30&timezone=America/New_York"
```

Default: Daily at 6:30 PM ET (after market close)

### Viewing Recommendations

- **Dashboard**: Latest recommendations for all stocks
- **Portfolio**: Holdings and watchlist management
- **Analytics**: AI accuracy metrics and performance tracking

### API Endpoints

Full API documentation available at: http://localhost:8000/docs

Key endpoints:
- `POST /api/analysis/{symbol}` - Analyze single stock
- `POST /api/analysis/batch` - Analyze all watchlist stocks
- `GET /api/portfolio/holdings` - Get portfolio
- `GET /api/performance/stats/accuracy` - Get AI accuracy stats

## 💰 Cost Optimization

### Gemini Model Selection

The application is configured to use cost-optimized Gemini models:

```python
# backend/services/trading_agents.py
config["quick_think_llm"] = "gemini-2.0-flash-lite"  # Analysts (cheaper)
config["deep_think_llm"] = "gemini-2.0-flash-exp"    # Trader/Risk (better reasoning)
```

### Estimated Monthly Costs (30 stocks, daily analysis)

| Model Configuration | Est. Cost/Month |
|---------------------|-----------------|
| Flash-Lite only | ~$67 |
| Flash-Lite + Flash | ~$150-250 |
| Flash + thinking mode | ~$250-400 |

### Cost Reduction Tips

1. **Reduce debate rounds**: Set `max_debate_rounds = 1` (default)
2. **Selective analysis**: Analyze only high-priority stocks
3. **Cache aggressively**: Price data cached for 24 hours
4. **Off-peak scheduling**: Run after market close when data is complete

## 🔒 Important Disclaimers

⚠️ **Investment Disclaimer**

> This application is designed for **research and educational purposes only**.
>
> - Do NOT make real trades based solely on AI recommendations
> - AI predictions may be inaccurate and should not be considered financial advice
> - Always do your own research and consult with financial professionals
> - Past performance does not guarantee future results

From TradingAgents documentation:
> "TradingAgents framework is designed for research purposes. Trading performance may vary. It is not intended as financial, investment, or trading advice."

## 📊 Database Schema

The application uses 5 main tables:

1. **watchlist** - Stocks being monitored
2. **decisions** - AI recommendations over time
3. **prices** - Historical market prices
4. **portfolio** - User holdings
5. **performance** - AI accuracy tracking

See `docs/supabase_schema.sql` for complete schema.

## 🛠️ Development

### Project Structure

```
deep-stock-agent/
├── backend/              # FastAPI application
│   ├── main.py          # Main application
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   ├── models/          # Pydantic schemas
│   └── db/              # Database operations
├── frontend/            # Next.js application
│   ├── app/            # App Router pages
│   ├── components/     # React components
│   └── lib/            # Utilities and API client
├── docs/               # Documentation
├── scripts/            # Setup scripts
└── TradingAgents/      # Cloned externally
```

### Adding New Features

1. **Backend endpoint**: Add to `backend/routers/`
2. **Database table**: Update `docs/supabase_schema.sql`
3. **Frontend page**: Add to `frontend/app/`
4. **API client**: Update `frontend/lib/api.ts`

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## 🐛 Troubleshooting

### TradingAgents Import Error

```
ImportError: No module named 'tradingagents'
```

**Solution**: Run the setup script:
```bash
./scripts/setup_tradingagents.sh
```

### Supabase Connection Error

```
Failed to connect to Supabase
```

**Solution**: Check your `.env` file:
- Ensure `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Verify your Supabase project is active (free tier pauses after 7 days)

### API Rate Limits

**Alpha Vantage**: Free tier = 5 calls/min, 500 calls/day
- Solution: Use caching, analyze in batches

**Gemini**: Monitor usage in Google Cloud Console
- Solution: Use Flash-Lite, reduce debate rounds

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review TradingAgents documentation

## 🙏 Acknowledgments

- [TradingAgents](https://github.com/JosephTLucas/TradingAgents) - Multi-agent LLM framework
- [LangChain](https://github.com/langchain-ai/langchain) - LLM orchestration
- [Gemini](https://ai.google.dev/) - Cost-effective LLM models
- [Supabase](https://supabase.com) - Backend as a service
- [Next.js](https://nextjs.org) - React framework
- [shadcn/ui](https://ui.shadcn.com) - UI components

---

Built with ❤️ for smarter portfolio monitoring
