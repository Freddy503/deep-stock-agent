# 🚀 Quick Setup Guide

## ✅ Completed Setup Steps

The following has been completed for you:

1. ✅ **Backend Dependencies Installed** - All Python packages in `venv/`
2. ✅ **Frontend Dependencies Installed** - All Node packages in `frontend/node_modules/`
3. ✅ **Environment Files Created**:
   - `backend/.env` (needs API keys)
   - `frontend/.env.local` (configured for localhost:8000)

## 🔑 Required API Keys

You need to obtain the following API keys and add them to `backend/.env`:

### 1. Google Gemini API Key (Required)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add to `backend/.env`:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### 2. Supabase (Required for Database)

1. Go to [Supabase](https://supabase.com)
2. Create a new project (free tier)
3. Go to Settings → API
4. Copy your credentials:
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=your_anon_key_here
   ```
5. Go to SQL Editor and run the schema from `docs/supabase_schema.sql`

### 3. Alpha Vantage (Optional)

1. Go to [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Get a free API key
3. Add to `backend/.env`:
   ```
   ALPHA_VANTAGE_API_KEY=your_key_here
   ```

## 🧬 TradingAgents Setup (Required)

You need to manually clone TradingAgents (can't do it in this environment):

```bash
# Clone TradingAgents in the project root
git clone https://github.com/JosephTLucas/TradingAgents.git

# Install TradingAgents dependencies
source venv/bin/activate
cd TradingAgents
pip install -r requirements.txt  # or pip install -e . if it has setup.py
cd ..
```

## 🏃 Running the Application

### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd /home/user/deep-stock-agent
source venv/bin/activate
cd backend
python main.py
```

Backend will start at: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd /home/user/deep-stock-agent/frontend
npm run dev
```

Frontend will start at: http://localhost:3000

### Option 2: Docker (if available)

```bash
# Make sure you've cloned TradingAgents first!
docker-compose up -d
```

## 📋 First Time Usage

1. **Open the app**: http://localhost:3000
2. **Add stocks to watchlist**:
   - Go to Portfolio page
   - Enter stock symbols (e.g., AAPL, GOOGL, MSFT)
   - Click "Add to Watchlist"
3. **Run analysis**:
   - Click "🤖 Run Analysis Now" on Dashboard
   - Wait for AI to analyze your stocks
   - View recommendations on Dashboard
4. **Set up schedule** (optional):
   - Configure daily analysis time via API or code
   - Default: 6:30 PM ET

## 🔍 Verify Setup

Run these checks:

```bash
# Check backend can import modules
source venv/bin/activate
python -c "from backend.models.schemas import DecisionResponse; print('✓ OK')"

# Check frontend builds
cd frontend
npm run build

# Check environment files
cat backend/.env | grep "GOOGLE_API_KEY"
cat frontend/.env.local | grep "NEXT_PUBLIC_API_URL"
```

## 📊 Supabase Database Schema

After creating your Supabase project, run this SQL:

```bash
# Copy the entire contents of this file and paste in Supabase SQL Editor
cat docs/supabase_schema.sql
```

This creates 5 tables:
- `watchlist` - Stocks to monitor
- `decisions` - AI recommendations
- `prices` - Historical price data
- `portfolio` - Your holdings
- `performance` - Accuracy tracking

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'tradingagents'"

**Solution**: You need to clone and install TradingAgents:
```bash
git clone https://github.com/JosephTLucas/TradingAgents.git
source venv/bin/activate
cd TradingAgents && pip install -e . && cd ..
```

### "Failed to connect to Supabase"

**Solution**:
1. Check `backend/.env` has correct `SUPABASE_URL` and `SUPABASE_KEY`
2. Ensure your Supabase project is active (free tier pauses after 7 days)
3. Run the schema from `docs/supabase_schema.sql` in Supabase SQL Editor

### "GOOGLE_API_KEY not set"

**Solution**: Add your Gemini API key to `backend/.env`

### Frontend can't connect to backend

**Solution**:
1. Make sure backend is running on port 8000
2. Check `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`

## 💰 Cost Estimate

With Gemini Flash/Flash-Lite and 30 stocks analyzed daily:

| Service | Cost/Month |
|---------|------------|
| Gemini API | $67-150 |
| Supabase (free tier) | $0 |
| Alpha Vantage (free) | $0 |
| **Total** | **~$67-150** |

Much cheaper than GPT-4 (~$500+/month)!

## 📚 Next Steps

1. ✅ Get your API keys
2. ✅ Clone TradingAgents
3. ✅ Run the Supabase schema
4. ✅ Start both backend and frontend
5. ✅ Add stocks and run your first analysis!

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review API docs at http://localhost:8000/docs
- Check TradingAgents documentation

---

**Important Reminder**: This system is for educational and research purposes only. Never make real trades based solely on AI recommendations. Always do your own research and consult with financial professionals.
