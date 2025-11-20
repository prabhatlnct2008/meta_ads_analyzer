# Meta Ads Analyzer

> AI-powered Facebook/Meta Ads analytics platform that helps businesses understand their ad performance in plain English.

## Overview

Meta Ads Analyzer is a SaaS application that connects to your Meta (Facebook/Instagram) advertising accounts and provides:

- **Clear Analytics**: Dashboard with key metrics (Spend, ROAS, CPA, CTR, Conversions)
- **AI-Powered Chat**: Ask questions about your performance and get actionable insights
- **Campaign Tracking**: Detailed breakdown of campaigns, ad sets, and ads
- **Smart Recommendations**: GPT-4 analyzes your data and suggests optimizations

## Features

- ✅ Secure Meta OAuth integration
- ✅ Multi-account support
- ✅ Real-time performance dashboards
- ✅ Interactive charts and visualizations
- ✅ AI chat assistant powered by GPT-4
- ✅ Campaign performance analysis
- ✅ Date range filtering (Last 7 days, 30 days, custom)
- ✅ Responsive design (mobile, tablet, desktop)

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Notifications**: react-hot-toast

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **API**: RESTful endpoints
- **Meta Integration**: Meta Marketing API v19.0
- **AI**: OpenAI GPT-4

### Deployment
- **Frontend**: Vercel
- **Backend**: PythonAnywhere (or any Python hosting)
- **Database**: SQLite (file-based)

## Quick Start

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python run.py
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local
npm run dev
```

Visit `http://localhost:3000` to see the app!

## Documentation

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Complete deployment guide
- **[prd.txt](./prd.txt)** - Product requirements document

## Project Structure

```
meta_ads_analyzer/
├── backend/          # Flask API
│   ├── app/         # Application code
│   └── run.py       # Entry point
├── frontend/        # Next.js app
│   ├── app/        # Pages
│   ├── components/ # React components
│   └── lib/        # Utilities
└── docs/           # Documentation
```

## Key Features

1. **Landing Page** - Beautiful marketing site
2. **Authentication** - Secure JWT-based auth
3. **Dashboard** - KPIs, charts, and insights
4. **Campaigns** - Detailed campaign analytics
5. **AI Chat** - GPT-4 powered assistant
6. **Settings** - Account management

## License

Proprietary - All rights reserved

---

**Built with ❤️ for advertisers who want better insights**
