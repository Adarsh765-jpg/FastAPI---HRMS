# ✅ Render Deployment Checklist

Use this checklist before deploying to Render.

## Pre-Deployment

- [ ] Code changes committed and pushed to GitHub/GitLab
- [ ] `requirements.txt` includes all dependencies
- [ ] Database fixes applied (`checkfirst=True` in database.py)
- [ ] Seeding logic prevents duplicates

## Render Configuration

### Build Settings
- [ ] Root Directory: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

### Environment Variables (CRITICAL!)
- [ ] `WEB_CONCURRENCY=1` ⚠️ MUST BE SET TO 1 FOR SQLITE
- [ ] `DATABASE_URL=sqlite:///./hrms.db`
- [ ] `JWT_SECRET_KEY=<your-secure-random-key>` ⚠️ CHANGE FROM DEFAULT
- [ ] `JWT_ALGORITHM=HS256`
- [ ] `JWT_EXPIRATION_HOURS=24`
- [ ] `CORS_ORIGINS=["https://your-frontend-url.com"]` ⚠️ UPDATE WITH YOUR FRONTEND URL

## Post-Deployment

- [ ] Service deployed successfully (check Render dashboard)
- [ ] Health check endpoint works: `https://your-app.onrender.com/`
- [ ] API docs accessible: `https://your-app.onrender.com/docs`
- [ ] Test login with default credentials:
  - Admin: `admin@example.com` / `admin123`
  - HR: `hr@example.com` / `hr123`
  - Employee: `employee@example.com` / `emp123`
- [ ] Check logs for any errors
- [ ] Test CORS by accessing from frontend

## Security Checklist

- [ ] Changed `JWT_SECRET_KEY` from default
- [ ] Updated default user passwords (or documented them securely)
- [ ] CORS origins restricted to your frontend domain only
- [ ] Database echo logs disabled (`echo=False`)

## Known Limitations (SQLite)

⚠️ **Remember:**
- Database resets on each deployment
- Single worker only (no horizontal scaling)
- Not suitable for high-traffic production

**Recommendation:** Migrate to PostgreSQL for production use.

---

## Quick Commands

**Generate secure JWT secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Test API locally before deploying:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Test login locally:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```
