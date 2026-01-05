# ⚡ START HERE - Your App is 99% Ready!

## ✅ What's Already Done:

1. ✅ **All your API keys configured** (Gemini, Supabase, Alpha Vantage)
2. ✅ **All dependencies installed** (Python + Node.js)
3. ✅ **Environment files ready**
4. ✅ **Deployment configs created** (Vercel ready)
5. ✅ **Everything pushed to GitHub**

## 🚀 Run Locally in 3 Commands:

### 1️⃣ Clone TradingAgents (30 seconds)
```bash
cd /home/user/deep-stock-agent
./CLONE_TRADINGAGENTS.sh
```

### 2️⃣ Set Up Database (2 minutes)
Go to: https://supabase.com/dashboard/project/gw1j95tgiy3dnu8kox1omq/sql

Click "SQL Editor" → Paste this file's contents → Run:
```bash
cat docs/supabase_schema.sql
```

### 3️⃣ Start the App! (2 terminals)

**Terminal 1:**
```bash
source venv/bin/activate
cd backend
python main.py
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

**Open:** http://localhost:3000

## 🎉 That's It! Use Your App:

1. Click **Portfolio** → Add "AAPL"
2. Go to **Dashboard** → Click "🤖 Run Analysis Now"
3. Wait 30 seconds → See AI recommendation!

---

## ☁️ Deploy to Vercel (5 minutes):

**Read this file:** `DEPLOY_TO_VERCEL.md`

**Quick version:**
1. Go to https://vercel.com/new
2. Import your GitHub repo: `Freddy503/deep-stock-agent`
3. Set Root Directory: `frontend`
4. Add environment variables (already have them!)
5. Deploy!

For backend: Use Railway.app (easier than Vercel for Python)

---

## 📁 Quick Reference:

- **RUN.md** - Detailed local setup
- **DEPLOY_TO_VERCEL.md** - Complete deployment guide
- **CLONE_TRADINGAGENTS.sh** - Helper to clone TradingAgents
- **START.sh** - Interactive start script

---

## 🆘 Problems?

### Can't clone TradingAgents?
```bash
cd /home/user/deep-stock-agent
git clone https://github.com/JosephTLucas/TradingAgents.git
cd TradingAgents && pip install -e . && cd ..
```

### Backend won't start?
```bash
source venv/bin/activate
cd backend
python main.py
```

### Database connection failed?
Did you run the SQL schema? See Step 2 above.

---

## 💰 What It Costs:

- **Local testing**: $0
- **Gemini API**: $67-150/month (for 30 stocks daily)
- **Hosting**: $0-5/month (Vercel free tier)
- **Total**: ~$67-155/month

**Much cheaper than GPT-4 (~$500/month)!**

---

## 🎯 Your Next Steps:

1. Run `./CLONE_TRADINGAGENTS.sh`
2. Set up Supabase database (copy SQL)
3. Start both servers
4. Test locally
5. Deploy to Vercel when ready

**Everything else is done!** 🚀
