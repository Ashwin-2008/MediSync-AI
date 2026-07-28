# Hospital Multi-Agent AI Coordination Platform

A massive, production-grade hospital coordination system powered by an intelligent swarm of specialized AI agents. This platform coordinates the complete patient workflow from intake to discharge.

## Architecture

The system consists of three main tiers:
1. **Frontend**: Premium React + Vite application with Tailwind CSS and Framer Motion, providing a futuristic, dark-mode medical dashboard.
2. **Backend**: High-performance FastAPI server backed by PostgreSQL, Redis, and Celery for async task processing.
3. **AI Swarm Engine**: A sophisticated multi-agent orchestrator with dynamic LLM provider routing (Gemini, OpenRouter, Qwen, DeepSeek, etc.) and intelligent fallback mechanisms.

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Framer Motion, React Query, React Router DOM, Lucide Icons.
- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL, Redis, Celery, JWT Auth.
- **AI Integration**: Custom Provider Routing Layer, API Key Rotation, and 10+ specific agent implementations.

## Setup Instructions

### 1. Environment Configuration

1. Navigate to `backend/`.
2. Update `backend/.env` with your actual LLM API keys:
   ```env
   GEMINI_KEY_1="your_key"
   OPENROUTER_KEY="your_key"
   # Add others as needed
   ```

### 2. Run with Docker Compose

To spin up the entire stack (PostgreSQL, Redis, Celery, FastAPI, and Vite):

```bash
docker-compose up --build
```

- **Frontend**: http://localhost:5173 (Requires uncommenting the frontend block in docker-compose.yml if you wish to run it in Docker)
- **Backend API Docs**: http://localhost:8000/docs
- **Database**: Port 5432
- **Redis**: Port 6379

### 3. Local Development (Alternative to full Docker)

If you prefer to run services locally (assuming Postgres/Redis are running via Docker):

**Backend**:
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # or venv/bin/activate on Mac/Linux
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

## AI Agents

The platform includes the following fully-implemented independent agents located in `backend/app/agents/`:
1. Patient Intake
2. Diagnosis
3. Medical History
4. Appointment
5. Treatment Planning
6. Lab
7. Pharmacy
8. Insurance
9. Billing
10. Discharge

Each agent operates autonomously, orchestrated by the `AgentOrchestrator`.

## Scalability & Production Readiness

- **Pluggable LLM Routing**: Requests are routed to simple, medium, or complex models automatically to balance cost, speed, and accuracy.
- **Resilience**: If a provider fails or rate-limits, the system falls back automatically (e.g., Gemini -> OpenRouter -> DeepSeek).
- **Asynchronous Execution**: Heavy AI tasks are offloaded to Celery workers backed by Redis.
- **Database Migrations**: Fully configured with Alembic.
