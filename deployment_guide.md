# 🚀 Deployment Guide

This guide explains how to deploy the HRMS application to a production environment.

## 1. Backend Deployment

### A. Environment Setup
1.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
2.  **CRITICAL:** Edit `.env` and change `JWT_SECRET_KEY` to a strong, random string.
    ```bash
    # Generate a strong key
    openssl rand -hex 32
    ```
3.  Update `CORS_ORIGINS` in `.env` to include your production frontend domain.

### B. Run with Uvicorn (Production Mode)
Do NOT use `--reload` in production. Use multiple workers for better performance.

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
*Note: On Windows, `gunicorn` is not supported. Use `uvicorn` directly:*
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 2. Frontend Deployment

### A. Build the Application
Vite compiles the React code into static HTML/CSS/JS files.

```bash
cd frontend
npm run build
```
This creates a `dist/` folder containing the production-ready files.

### B. Serve the Static Files
You can serve the `dist/` folder using any static file server (Nginx, Apache, AWS S3, Netlify, Vercel).

**Example: Using `serve` (Node.js)**
```bash
npm install -g serve
serve -s dist -l 5173
```

---

## 3. Database (SQLite vs PostgreSQL)

By default, the app uses **SQLite** (`hrms.db`).
- **Pros:** Zero setup, easy to backup (just copy the file).
- **Cons:** Not suitable for high concurrency or multiple backend instances.

**For High Traffic:**
1.  Install PostgreSQL.
2.  Update `DATABASE_URL` in `.env`:
    ```
    DATABASE_URL=postgresql://user:password@localhost/dbname
    ```
3.  Install driver: `pip install psycopg2-binary`

---

## 4. Security Checklist ✅

- [ ] **Secret Key:** Changed `JWT_SECRET_KEY` in `.env`.
- [ ] **Debug:** Ensure `reload` is OFF.
- [ ] **CORS:** Only allow trusted domains.
- [ ] **HTTPS:** Serve both Frontend and Backend over HTTPS (using Nginx/Certbot or Cloudflare).
