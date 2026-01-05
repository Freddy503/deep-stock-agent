# 🚀 Deploy to Vercel - Complete Guide

## Prerequisites

✅ Tested locally and working
✅ Supabase database set up
✅ All API keys working

## Step 1: Prepare Your Repository

Your code is already on GitHub in the branch: `claude/portfolio-monitoring-system-644sw`

You need to merge it to main or create a release branch:

```bash
# Option A: Merge to main
git checkout main
git merge claude/portfolio-monitoring-system-644sw
git push origin main

# Option B: Create production branch
git checkout -b production
git merge claude/portfolio-monitoring-system-644sw
git push origin production
```

## Step 2: Install Vercel CLI (Optional but Recommended)

```bash
npm install -g vercel
```

## Step 3: Deploy to Vercel

### Option A: Via Vercel Dashboard (Easiest)

1. Go to: https://vercel.com/new
2. Import your GitHub repository: `Freddy503/deep-stock-agent`
3. Select branch: `main` or `production`
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. Add Environment Variables:
   ```
   GOOGLE_API_KEY=AIzaSyD_hY8YxNeqJWM7zlgw0zDPyWhUKvyqQek
   ALPHA_VANTAGE_API_KEY=C552K0AL5LTEI272
   SUPABASE_URL=https://gw1j95tgiy3dnu8kox1omq.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
   ```

6. Click **Deploy**

### Option B: Via CLI

```bash
cd /home/user/deep-stock-agent

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## Step 4: Deploy Backend Separately

Vercel is primarily for frontend. For the backend, you have 2 options:

### Option 1: Vercel Serverless Functions (Simple but Limited)

The backend can run on Vercel serverless, but:
- ⚠️ TradingAgents might be too large for serverless
- ⚠️ Cold starts will be slow
- ⚠️ 10-second execution limit

To try:
1. Move `backend/main.py` to `api/index.py`
2. Add `requirements.txt` to project root
3. Deploy normally

### Option 2: Railway.app (Recommended for Backend)

Railway is better for the FastAPI backend:

1. Go to: https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `python main.py`
   - **Environment Variables**: Same as above

5. Railway will give you a URL like: `https://deep-stock-agent.up.railway.app`

6. Update Vercel environment:
   ```
   NEXT_PUBLIC_API_URL=https://deep-stock-agent.up.railway.app
   ```

### Option 3: Render.com (Alternative)

1. Go to: https://render.com
2. Create new "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment Variables**: Add all API keys

## Step 5: Update CORS

Once deployed, update `backend/.env`:

```env
CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:3000
```

Redeploy backend.

## Step 6: Test Production

1. Visit your Vercel URL
2. Add a stock to watchlist
3. Run analysis
4. Check if AI recommendations appear

## 📊 Recommended Architecture

```
┌─────────────────────────────────────────┐
│   Frontend (Vercel)                     │
│   https://stocks.vercel.app             │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│   Backend (Railway/Render)              │
│   https://api.railway.app               │
└─────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│   Database (Supabase)                   │
│   Already configured ✅                 │
└─────────────────────────────────────────┘
```

## 💰 Estimated Costs

| Service | Free Tier | Paid (if needed) |
|---------|-----------|------------------|
| Vercel (Frontend) | 100GB bandwidth | $20/month |
| Railway (Backend) | $5 credit | $5-10/month |
| Supabase | 500MB database | $25/month |
| Gemini API | Pay per use | $67-150/month |
| **Total** | **~$0-5/month** | **~$117-205/month** |

## 🔒 Security Notes

Before deploying:

1. **Never commit .env files** (already in .gitignore ✅)
2. **Use Vercel environment variables** for secrets
3. **Enable Supabase RLS** (Row Level Security)
4. **Add rate limiting** to backend API
5. **Use HTTPS only** (Vercel handles this ✅)

## 🚨 Production Checklist

- [ ] Merged to production branch
- [ ] Supabase schema deployed
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Railway/Render
- [ ] Environment variables set
- [ ] CORS configured
- [ ] Tested adding stocks
- [ ] Tested running analysis
- [ ] Tested on mobile
- [ ] Set up monitoring (Vercel Analytics)

## ⚡ Quick Deploy Commands

```bash
# Frontend to Vercel
cd frontend
vercel --prod

# Backend to Railway (after setting up Railway CLI)
cd backend
railway up

# Or use their web dashboards - much easier!
```

## 🆘 Common Issues

### "API not responding"
→ Check backend URL in Vercel environment variables

### "CORS error"
→ Add Vercel URL to backend CORS_ORIGINS

### "Serverless timeout"
→ Backend is too slow for Vercel - use Railway/Render instead

### "Too large to deploy"
→ TradingAgents is big - use Railway with Docker

## 📚 Resources

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Next.js Deploy: https://nextjs.org/docs/deployment

---

## ✨ Easiest Path to Production:

1. **Frontend**: Deploy to Vercel (takes 2 minutes)
2. **Backend**: Deploy to Railway (takes 5 minutes)
3. **Database**: Already on Supabase ✅
4. **Done!** Your app is live 🎉
