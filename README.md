# Smart Goal Breaker

AI-powered goal breakdown application with multi-user support.

## 🚀 Features

- **AI Goal Breakdown**: Uses Gemini AI to break vague goals into 5 actionable steps
- **Multi-User Support**: Session-based isolation - each user sees only their goals
- **Delete Functionality**: Remove goals with ownership verification
- **Modern Stack**: FastAPI + Next.js + PostgreSQL
- **Deployment Ready**: Configured for Vercel (frontend) + Render (backend)

## 📁 Project Structure

```
smart-goal-breaker/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py           # API endpoints
│   │   ├── models.py         # Database models
│   │   ├── ai_service.py     # Gemini integration
│   │   └── session.py        # Session management
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # Next.js application
│   ├── src/
│   │   ├── app/              # Pages
│   │   ├── components/       # React components
│   │   └── lib/              # API client
│   └── package.json
└── docker-compose.yml        # PostgreSQL database
```

## 🛠️ Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Docker Desktop
- Gemini API Key ([get one here](https://makersuite.google.com/app/apikey))

### 1. Start Database
```bash
docker-compose up -d
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your Gemini API key to .env
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_key_here

# Start server
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend
npm install  # If not already installed
npm run dev
```

Frontend runs at `http://localhost:3000`

## 🧪 Testing Multi-User Isolation

1. Open app in **Chrome**: `http://localhost:3000`
2. Create a goal (e.g., "Learn guitar")
3. Open app in **Firefox** or **Incognito**: `http://localhost:3000`
4. Create a different goal (e.g., "Launch startup")
5. Verify each browser shows only its own goals

## 🚢 Deployment

### Backend (Render)
1. Create PostgreSQL database on Render
2. Create Web Service with:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment: `DATABASE_URL`, `GEMINI_API_KEY`

### Frontend (Vercel)
1. Import repository
2. Root directory: `frontend`
3. Environment: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api`

### Post-Deployment
Update CORS in `backend/app/main.py` to include your Vercel domain.

## 📚 API Endpoints

- `POST /api/goals` - Create goal with AI breakdown
- `GET /api/goals` - Get user's goals
- `DELETE /api/goals/{id}` - Delete goal

## 🔒 How Sessions Work

- Each user gets a UUID session ID stored in a cookie
- All goals are filtered by session ID
- No authentication needed - perfect for prototyping
- Users can only see and delete their own goals

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Gemini AI
- **Frontend**: Next.js 14, React, TypeScript, shadcn/ui
- **Database**: PostgreSQL (Docker)
- **Deployment**: Vercel + Render

## 📝 License

MIT
