# 🚀 HOW TO RUN - Super Simple Steps

## ✅ Everything is Ready! Just 3 Commands:

### Step 1: Clone TradingAgents (One Time Only)
```bash
cd /home/user/deep-stock-agent
git clone https://github.com/JosephTLucas/TradingAgents.git
cd TradingAgents
pip install -e .
cd ..
```

### Step 2: Set Up Supabase Database (One Time Only)
1. Go to: https://supabase.com/dashboard/project/gw1j95tgiy3dnu8kox1omq/sql
2. Click "SQL Editor"
3. Copy ALL the SQL from `docs/supabase_schema.sql`
4. Paste and click "Run"
5. You should see: "Success. No rows returned"

### Step 3: Run the App!

**Open 2 terminals in this directory:**

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
cd backend
python main.py
```
✅ You'll see: "Application started successfully!"
🌐 Backend running at: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
✅ You'll see: "Local: http://localhost:3000"
🌐 Frontend running at: http://localhost:3000

### Step 4: Use It!

1. **Open browser**: http://localhost:3000
2. **Go to Portfolio** page
3. **Add a stock**: Type "AAPL" and click "Add to Watchlist"
4. **Go to Dashboard**
5. **Click** "🤖 Run Analysis Now"
6. **Wait** ~30 seconds for AI to analyze
7. **See results!** AI will show BUY/SELL/HOLD recommendation

---

## 🎉 That's It!

Your stock portfolio monitor is now running with AI-powered recommendations!

## 🔍 What You Can Do:

- **Dashboard**: View all AI recommendations
- **Portfolio**: Add/remove stocks, view holdings
- **Analytics**: See AI accuracy over time

## 📊 API Documentation

Once backend is running, visit: http://localhost:8000/docs

---

## 🚨 Troubleshooting

### "ModuleNotFoundError: No module named 'tradingagents'"
→ You forgot Step 1. Clone TradingAgents:
```bash
git clone https://github.com/JosephTLucas/TradingAgents.git
cd TradingAgents && pip install -e . && cd ..
```

### Backend won't start
→ Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

### Frontend errors
→ Make sure you're in the frontend directory:
```bash
cd frontend
npm run dev
```

### "Failed to connect to Supabase"
→ Did you run the SQL schema? See Step 2 above.

---

## ⚡ Quick Start (All in One)

If you just want to run everything at once:

```bash
# Make sure you cloned TradingAgents first!
./START.sh
```

Choose option 3 to start both services.
