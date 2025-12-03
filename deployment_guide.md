# 🚀 Deployment Guide

This guide explains how to deploy the HRMS application to production.

## ⚠️ Critical: SQLite + Multi-Worker Issue

**IMPORTANT:** SQLite does not handle multiple workers well. You have two options:

### Option A: Use 1 Worker (Simpler, but less scalable)
```bash
gunicorn app.main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000
```

Or even simpler:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

### Option B: Switch to PostgreSQL (Recommended for production)
1. Get a PostgreSQL database (Render provides free PostgreSQL)
2. Set `DATABASE_URL` environment variable to your Postgres connection string
3. Use multiple workers for better performance:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000
```

---

## 1. Backend Deployment (Render.com)

### A. Environment Setup
These environment variables MUST be set on Render:

| Variable | Value | Required |
|----------|-------|----------|
| `JWT_SECRET_KEY` | (see backend/.env for your random key) | ✅ Yes |
| `CORS_ORIGINS` | `["https://your-frontend.vercel.app"]` | ✅ Yes |
| `DATABASE_URL` | Auto-provided by Render if using Postgres | No (defaults to SQLite) |
| `DATABASE_ECHO` | `False` | No (defaults to False) |
| `PYTHON_VERSION` | `3.10.0` | Recommended |

### B. Render Settings

```yaml
Name: hrms-backend
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000
```

> **Note:** Using single-process uvicorn because of SQLite. If you add PostgreSQL, use:
> `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000`

### C. What Happens on Deploy
1. Render installs dependencies
2. App starts and creates database tables
3. `seed_database()` runs automatically:
   - If database is empty, creates Admin/HR/Employee users
   - If Admin exists, resets password to `admin123`

---

## 2. Frontend Deployment (Vercel)

### A. Build Configuration

```yaml
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
Root Directory: frontend
```

### B. Environment Variables on Vercel

| Variable | Value | Example |
|----------|-------|---------|
| `VITE_API_URL` | Your backend URL | `https://hrms-backend.onrender.com` |

### C. After Deploy
1. Get your Vercel URL (e.g., `https://hrms-frontend.vercel.app`)
2. Go back to Render
3. Update `CORS_ORIGINS` to include your Vercel URL:
   ```json
   ["https://hrms-frontend.vercel.app"]
   ```
4. Click "Manual Deploy" → "Clear build cache & deploy"

---

## 3. Database Options

### SQLite (Default)
- ✅ Zero configuration
- ✅ Easy backup (just copy the file)
- ❌ **Must use 1 worker**
- ❌ Not suitable for high traffic

### PostgreSQL (Recommended for Production)

**On Render:**
1. Dashboard → New → PostgreSQL
2. Create database (free tier available)
3. Copy the "Internal Database URL"
4. Add to your web service as `DATABASE_URL` environment variable
5. Restart service - it will auto-create tables

> **Migration Note:** Switching from SQLite to Postgres will start with an empty database.
> The seed script will auto-populate it with default users.

---

## 4. Security Checklist ✅

Before deploying to production:

- [ ] **Changed** `JWT_SECRET_KEY` to a strong random value
- [ ] **Updated** `CORS_ORIGINS` to only include your production frontend
- [ ] **Removed** `--reload` flag from start command
- [ ] **Configured** HTTPS (Render and Vercel provide this automatically)
- [ ] **Tested** login with `admin@example.com` / `admin123`
- [ ] **Verified** RBAC works (HR can only create employees)

---

## 5. Monitoring & Debugging

### Enable SQL Query Logging
Set environment variable:
```
DATABASE_ECHO=true
```
This will log all SQL queries (useful for debugging, disable in production)

### Check Application Logs
**Render:** Click on your service → Logs tab
**Vercel:** Click on your deployment → Function logs

### Common Issues

#### "401 Unauthorized" / Can't Login
- **Cause:** Database seed didn't run or password mismatch
- **Fix:** Check logs for "Database seeded successfully!" or "Admin password reset"
- **Manual Fix:**
  1. SSH into Render (if possible) or use database explorer
  2. Run: `python -m app.seed_data`

#### "Table already exists" Error
- **Cause:** Running with multiple workers + SQLite
- **Fix:** Use 1 worker OR switch to PostgreSQL

#### CORS Error in Browser
- **Cause:** Frontend URL not in CORS_ORIGINS
- **Fix:**
  1. Add frontend URL to `CORS_ORIGINS` env var on Render
  2. Format: `["https://your-frontend.vercel.app"]`
  3. Redeploy backend

---

## 6. Performance Tips

1. **Use PostgreSQL** instead of SQLite for >50 concurrent users
2. **Enable multiple workers** once on Postgres (4 workers recommended)
3. **Add Redis** for session/cache management (future enhancement)
4. **Enable gzip compression** (Render does this automatically)
5. **Monitor response times** and add database indexes if queries are slow

---

## 7. Backup & Recovery

### SQLite Backup
```bash
# Download hrms.db file from Render disk (if persistent disk attached)
# Or use database explorer to export
```

### PostgreSQL Backup
Render provides automated daily backups for paid plans.
For free tier, use pg_dump or export via database explorer.

---

## 🎉 Deployment Complete!

Your HRMS application should now be live at:
- **Frontend:** https://your-app.vercel.app
- **Backend:** https://your-api.onrender.com
- **API Docs:** https://your-api.onrender.com/docs

**Default Login:**
```
Email: admin@example.com
Password: admin123
```

> ⚠️ **Important:** Change these credentials in production!
