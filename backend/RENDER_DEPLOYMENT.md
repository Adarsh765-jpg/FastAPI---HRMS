# 🚀 Render Deployment Guide (SQLite Option)

This guide will help you deploy your HRMS backend to Render using SQLite.

## ⚠️ Important: SQLite Limitations on Render

SQLite works on Render but has limitations:
- **Single worker only** - Multiple workers will cause database locking issues
- **Data persistence** - Database resets on each deployment (use PostgreSQL for production)
- **Performance** - Not ideal for high-traffic applications

## 📋 Step-by-Step Deployment

### 1. Create a New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub/GitLab repository
4. Select your repository

### 2. Configure Build Settings

**Basic Settings:**
- **Name:** `hrms-backend` (or your preferred name)
- **Region:** Choose closest to your users
- **Branch:** `main` (or your deployment branch)
- **Root Directory:** `backend`
- **Runtime:** `Python 3`

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 3. Set Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** and add these:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | `sqlite:///./hrms.db` | SQLite database file |
| `JWT_SECRET_KEY` | `your-random-secret-key-here` | ⚠️ Generate a secure random string! |
| `JWT_ALGORITHM` | `HS256` | Default algorithm |
| `JWT_EXPIRATION_HOURS` | `24` | Token expiration time |
| `CORS_ORIGINS` | `["https://your-frontend.com"]` | Your frontend URL |
| `WEB_CONCURRENCY` | `1` | ⚠️ CRITICAL: Must be 1 for SQLite |
| `PYTHON_VERSION` | `3.11.0` | Optional: Specify Python version |

**🔐 Generate a Secure JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Configure Instance Settings

- **Instance Type:** Free (or paid for better performance)
- **Auto-Deploy:** Enable (deploys automatically on git push)

### 5. Deploy!

Click **"Create Web Service"** and wait for deployment to complete.

## ✅ Verify Deployment

Once deployed, test your API:

1. **Health Check:**
   ```
   https://your-app.onrender.com/
   ```
   Should return: `{"status": "ok", ...}`

2. **API Documentation:**
   ```
   https://your-app.onrender.com/docs
   ```
   Interactive Swagger UI

3. **Test Login:**
   ```bash
   curl -X POST https://your-app.onrender.com/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@example.com","password":"admin123"}'
   ```

## 🔧 Troubleshooting

### Issue: "table employees already exists"
**Solution:** Already fixed in code with `checkfirst=True`

### Issue: Multiple workers causing errors
**Solution:** Ensure `WEB_CONCURRENCY=1` is set in environment variables

### Issue: Database resets on deployment
**Solution:** This is expected with SQLite on Render. Upgrade to PostgreSQL for persistence.

### Issue: CORS errors from frontend
**Solution:** Add your frontend URL to `CORS_ORIGINS` environment variable

## 📊 Monitoring

- **Logs:** View real-time logs in Render dashboard
- **Metrics:** Monitor CPU, memory, and request metrics
- **Alerts:** Set up email alerts for service failures

## 🔄 Updating Your App

1. Push changes to your git repository
2. Render auto-deploys (if enabled)
3. Monitor deployment logs for any errors

## ⬆️ Upgrade to PostgreSQL (Recommended)

For production use, switch to PostgreSQL:

1. Create a PostgreSQL database on Render (free tier available)
2. Update `DATABASE_URL` environment variable to PostgreSQL connection string
3. Remove SQLite-specific config from `database.py`
4. Increase `WEB_CONCURRENCY` to 4 for better performance

See `POSTGRESQL_MIGRATION.md` for detailed migration steps.

## 📞 Support

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- Check your application logs in Render dashboard for errors
