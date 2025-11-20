# Meta Ads Analyzer - Deployment Guide

Complete deployment guide for Meta Ads Analytics SaaS application.

## Architecture Overview

- **Frontend**: Next.js + React + TypeScript + Tailwind CSS (Deployed on Vercel)
- **Backend**: Flask + Python (Deployed on PythonAnywhere)
- **Database**: SQLite (on PythonAnywhere)
- **LLM**: OpenAI GPT-4
- **Meta Integration**: Meta Marketing API v19.0

---

## Prerequisites

1. **Meta Developer Account**
   - Create a Meta app at https://developers.facebook.com/
   - Get App ID and App Secret
   - Request `ads_read` and `ads_management` permissions

2. **OpenAI Account**
   - Get API key from https://platform.openai.com/

3. **Vercel Account**
   - Sign up at https://vercel.com/

4. **PythonAnywhere Account**
   - Sign up at https://www.pythonanywhere.com/

---

## Part 1: Backend Deployment (PythonAnywhere)

### Step 1: Upload Code to PythonAnywhere

1. **Clone or upload your code**
   ```bash
   cd ~
   git clone <your-repo-url> meta_ads_analyzer
   cd meta_ads_analyzer/backend
   ```

2. **Create virtual environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 meta_ads_env
   workon meta_ads_env
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Configure Environment Variables

Create `/home/yourusername/meta_ads_analyzer/backend/.env`:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_SECRET_KEY=<generate-a-strong-secret-key>
PORT=5000

# Database
DATABASE_URL=sqlite:////home/yourusername/meta_ads_analyzer/backend/meta_ads_analyzer.db

# JWT
JWT_SECRET=<generate-a-strong-jwt-secret>

# Encryption
ENCRYPTION_SECRET=<generate-a-strong-encryption-secret>

# Meta/Facebook
META_APP_ID=your-meta-app-id
META_APP_SECRET=your-meta-app-secret
META_REDIRECT_URI=https://yourusername.pythonanywhere.com/api/meta/callback

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview

# Frontend URL (for CORS)
FRONTEND_URL=https://your-vercel-app.vercel.app
```

### Step 3: Initialize Database

```bash
workon meta_ads_env
cd /home/yourusername/meta_ads_analyzer/backend
python -c "from app import create_app; from app.database import db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### Step 4: Configure WSGI

Create `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import sys
import os
from dotenv import load_dotenv

# Add your project directory to the sys.path
project_home = '/home/yourusername/meta_ads_analyzer/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
load_dotenv(os.path.join(project_home, '.env'))

# Import your Flask app
from app import create_app
application = create_app()
```

### Step 5: Configure Web App in PythonAnywhere

1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration** → **Python 3.10**
4. Set **Source code** to: `/home/yourusername/meta_ads_analyzer/backend`
5. Set **Working directory** to: `/home/yourusername/meta_ads_analyzer/backend`
6. Set **Virtualenv** to: `/home/yourusername/.virtualenvs/meta_ads_env`
7. Edit **WSGI configuration file** (as shown above)
8. Click **Reload** button

### Step 6: Test Backend

Visit: `https://yourusername.pythonanywhere.com/health`

Should return: `{"status": "healthy", "message": "Meta Ads Analyzer API is running"}`

---

## Part 2: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Deployment

1. **Create `.env.local` file** (for local testing):
   ```bash
   NEXT_PUBLIC_API_URL=https://yourusername.pythonanywhere.com
   ```

2. **Update `next.config.js`** to handle API calls:
   ```javascript
   /** @type {import('next').NextConfig} */
   const nextConfig = {
     async rewrites() {
       return [
         {
           source: '/api/:path*',
           destination: process.env.NEXT_PUBLIC_API_URL + '/api/:path*',
         },
       ];
     },
   };

   module.exports = nextConfig;
   ```

### Step 2: Deploy to Vercel

#### Option A: Via Vercel Dashboard

1. Go to https://vercel.com/new
2. Import your Git repository
3. Set **Root Directory** to `frontend`
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL=https://yourusername.pythonanywhere.com`
5. Click **Deploy**

#### Option B: Via Vercel CLI

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

When prompted:
- Set root directory to `frontend`
- Add environment variables

### Step 3: Configure Environment Variables in Vercel

In Vercel Dashboard → Your Project → Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://yourusername.pythonanywhere.com
```

---

## Part 3: Meta App Configuration

### Step 1: Configure OAuth Redirect URLs

In Meta Developer Console → Your App → Settings → Basic:

1. Add **App Domains**:
   - `pythonanywhere.com`
   - `vercel.app`

2. In **Facebook Login** → Settings:
   - Add **Valid OAuth Redirect URIs**:
     - `https://yourusername.pythonanywhere.com/api/meta/callback`

### Step 2: Request Permissions

1. Go to **App Review** → **Permissions and Features**
2. Request:
   - `ads_read`
   - `ads_management`
   - `business_management`

---

## Part 4: Testing the Full Application

### Test Checklist

1. **Backend Health Check**
   - [ ] Visit `https://yourusername.pythonanywhere.com/health`
   - [ ] Should return healthy status

2. **Frontend Access**
   - [ ] Visit `https://your-app.vercel.app`
   - [ ] Landing page loads correctly

3. **User Registration**
   - [ ] Sign up with email/password
   - [ ] Receive JWT token
   - [ ] Redirect to dashboard

4. **Meta Connection**
   - [ ] Click "Connect Facebook Ads"
   - [ ] Meta OAuth flow works
   - [ ] Redirected back to dashboard
   - [ ] Accounts appear in dropdown

5. **Dashboard**
   - [ ] KPIs load correctly
   - [ ] Charts render
   - [ ] Date range selector works

6. **Campaigns Page**
   - [ ] Campaigns table loads
   - [ ] Data displays correctly

7. **Chat Feature**
   - [ ] Create new conversation
   - [ ] Send message
   - [ ] Receive AI response

8. **Settings**
   - [ ] View connected accounts
   - [ ] Disconnect account works
   - [ ] Refresh account works

---

## Part 5: Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `FLASK_SECRET_KEY` | Flask session secret | Random string |
| `DATABASE_URL` | SQLite database path | `sqlite:///path/to/db` |
| `JWT_SECRET` | JWT signing secret | Random string |
| `ENCRYPTION_SECRET` | Token encryption secret | Random string |
| `META_APP_ID` | Meta app ID | From Meta Developer |
| `META_APP_SECRET` | Meta app secret | From Meta Developer |
| `META_REDIRECT_URI` | OAuth callback URL | Backend URL + `/api/meta/callback` |
| `OPENAI_API_KEY` | OpenAI API key | From OpenAI |
| `OPENAI_MODEL` | GPT model to use | `gpt-4-turbo-preview` |
| `FRONTEND_URL` | Frontend URL for CORS | Vercel app URL |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | PythonAnywhere URL |

---

## Part 6: Troubleshooting

### Issue: CORS Errors

**Solution**: Ensure `FRONTEND_URL` in backend `.env` matches your Vercel deployment URL.

### Issue: OAuth Redirect Not Working

**Solution**:
1. Check `META_REDIRECT_URI` in backend `.env`
2. Verify redirect URI is added in Meta app settings
3. Ensure callback URL uses HTTPS

### Issue: Database Not Found

**Solution**:
1. Check `DATABASE_URL` path is absolute
2. Ensure database file exists: `ls -la /home/yourusername/meta_ads_analyzer/backend/meta_ads_analyzer.db`
3. Re-initialize: Run database initialization script

### Issue: 500 Internal Server Error

**Solution**:
1. Check PythonAnywhere error logs: **Web** tab → **Error log**
2. Verify all environment variables are set
3. Check virtualenv is activated in WSGI config

### Issue: OpenAI API Errors

**Solution**:
1. Verify `OPENAI_API_KEY` is correct
2. Check API quota/billing
3. Ensure model name is valid

---

## Part 7: Monitoring & Maintenance

### Logs

**Backend Logs** (PythonAnywhere):
- Web tab → Error log
- Web tab → Server log
- Access log

**Frontend Logs** (Vercel):
- Vercel Dashboard → Your Project → Deployments → View Function Logs

### Database Backups

Schedule regular backups of SQLite database:

```bash
#!/bin/bash
# Backup script for PythonAnywhere
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/yourusername/backups"
DB_PATH="/home/yourusername/meta_ads_analyzer/backend/meta_ads_analyzer.db"

mkdir -p $BACKUP_DIR
cp $DB_PATH $BACKUP_DIR/meta_ads_analyzer_$DATE.db
# Keep only last 7 backups
ls -t $BACKUP_DIR/meta_ads_analyzer_*.db | tail -n +8 | xargs rm -f
```

### Updates

**Backend Updates**:
```bash
cd /home/yourusername/meta_ads_analyzer/backend
git pull origin main
workon meta_ads_env
pip install -r requirements.txt
# Reload web app in PythonAnywhere dashboard
```

**Frontend Updates**:
```bash
git push origin main  # Vercel auto-deploys on push
```

---

## Part 8: Security Checklist

- [ ] All secrets are in `.env` files (not committed to Git)
- [ ] `.env` files are in `.gitignore`
- [ ] HTTPS is enabled for both frontend and backend
- [ ] JWT secrets are strong random strings (min 32 chars)
- [ ] Meta app is in production mode (not development)
- [ ] Database backups are scheduled
- [ ] CORS is configured to allow only your frontend domain
- [ ] Meta access tokens are encrypted in database
- [ ] Rate limiting is considered for API endpoints

---

## Support & Resources

- **Meta Marketing API Docs**: https://developers.facebook.com/docs/marketing-apis
- **Next.js Docs**: https://nextjs.org/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **Vercel Docs**: https://vercel.com/docs
- **PythonAnywhere Docs**: https://help.pythonanywhere.com/

---

## Quick Start Summary

1. **Backend**: Deploy to PythonAnywhere, configure `.env`, initialize database
2. **Frontend**: Deploy to Vercel with `NEXT_PUBLIC_API_URL` env var
3. **Meta App**: Configure OAuth redirect URLs
4. **Test**: Complete the test checklist above

**You're ready to go! 🚀**
