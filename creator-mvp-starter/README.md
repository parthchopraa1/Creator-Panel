# Creator Analytics MVP — Free-Plan Starter

A lean, **consent-first** starter to aggregate creator data (YouTube first), show a unified dashboard, and generate AI suggestions — all on **free tiers**.

> This starter includes: a minimal FastAPI backend with YouTube OAuth routes, token encryption, Postgres schema, GitHub Actions template, and deployment notes for Render + Supabase. Frontend is a placeholder; start with Vercel + React later.

---

## 🧭 Roadmap (first 2 weeks)

**Day 1–2**
1) Create a free **Supabase** project (or Neon) → get `DATABASE_URL`  
2) Fork this repo and add Render **Free Web Service** → set environment from `.env.example`  
3) In **Google Cloud Console**: create a project → OAuth consent screen (External) → Credentials → OAuth Client (Web).  
   - Add redirect URI: `https://<your-backend>.onrender.com/auth/youtube/callback`  
   - Copy client id/secret to `.env`

**Day 3–4**
4) Deploy backend on Render Free.  
5) Hit `/health` to verify.  
6) Visit `/auth/youtube/start` in the browser → complete Google OAuth → get redirected to callback.  
7) Check logs: tokens stored encrypted, connector row created.

**Day 5–7**
8) Implement a simple CRON (APScheduler) to refresh metrics daily.  
9) Build a basic React dashboard on **Vercel Free** that calls `/me/summary`.  
10) Add **Export All** and **Delete All** endpoints.

**Week 2**
11) Instagram Graph API in dev mode (invite your IG Creator account as tester).  
12) Patreon OAuth for earnings.  
13) First AI suggestions (heuristics) — return 3 cards.

---

## 🔐 Consent text (copy-paste)

**YouTube (Google):**  
> We will read your YouTube channel analytics (views, watch time, impressions, estimated revenue) to show you a unified dashboard and personalized recommendations. We store your access token encrypted. You can disconnect and delete your data at any time from Settings.

**Instagram (Meta Creator/Business):**  
> We will read your Instagram insights (reach, impressions, engagement) for your Creator/Business account to show performance across platforms. We store your token encrypted. You can disconnect and delete your data at any time from Settings.

**Patreon:**  
> We will read your creator earnings and membership stats to include Patreon data in your dashboard. We store your token encrypted. You can disconnect and delete your data at any time from Settings.

---

## 🧰 Local development

```bash
# Python 3.11+ recommended
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

# Create a .env from the example and fill credentials
cp .env.example .env

# Create tables
psql "$DATABASE_URL" -f sql/schema.sql

# Run the API
uvicorn app.main:app --reload --port 8000 --app-dir backend
```

### Handy commands
```bash
# Generate an ENCRYPTION_KEY for token storage
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## 🚀 Deploy (Free tiers)

**Backend (Render Free Web Service)**  
- Build: `pip install -r backend/requirements.txt`  
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir backend`  
- Add env vars from `.env` (never commit secrets).

**DB (Supabase/Neon Free)**  
- Paste `sql/schema.sql` in SQL editor.  
- Copy the provided `DATABASE_URL` to Render env.

**Frontend (later)**  
- Use Vercel Free with a React app (Vite). Point it at your backend base URL.

---

## 📦 API Overview (initial)

- `GET /health` → health check  
- `GET /auth/youtube/start` → begin OAuth (redirects to Google)  
- `GET /auth/youtube/callback?code=...` → exchange token, save connector  
- `GET /me/summary` → stubbed summary (extend after ingestion)  
- `DELETE /data/delete` → deletes connectors + raw payloads for your user

---

## 🗄️ Database Schema

See `sql/schema.sql` — minimal tables: `users`, `connectors`, `posts`, `metrics_aggregates`, `recommendations`.

---

## ⚙️ Next Steps

- Add APScheduler job to refresh channel + recent videos daily.  
- Normalize metrics into `metrics_aggregates`.  
- Implement `GET /recommendations` (3 heuristic cards).  
- Build a simple React dashboard to call these endpoints.

> This is a starter — keep scopes minimal, encrypt tokens, and provide Export/Delete controls.
