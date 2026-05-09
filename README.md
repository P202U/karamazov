```
karamazov/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ ├── v1/
│ │ │ │ ├── __init__.py
│ │ │ │ ├── interviews.py # Main logic loop (Next Question)
│ │ │ │ ├── uploads.py # Resume/JD ingestion
│ │ │ │ └── feedback.py # STAR report retrieval
│ │ │ └── deps.py # Dependency injection (DB session)
│ │ ├── core/
│ │ │ ├── config.py # uv-ready env config (pydantic-settings)
│ │ │ ├── prompts.py # Personas (Recruiter, STAR Judge)
│ │ │ └── security.py # Auth/Security logic
│ │ ├── db/
│ │ │ ├── session.py # SQLAlchemy engine & session
│ │ │ └── init_db.py # Table creation scripts
│ │ ├── models/ # SQLAlchemy/SQLModel (DB Tables)
│ │ │ ├── base.py
│ │ │ ├── interview.py # Interview session table
│ │ │ └── message.py # Message history + JSONB Analysis
│ │ ├── schemas/ # Pydantic (Request/Response contracts)
│ │ │ ├── interview.py
│ │ │ └── feedback.py # STAR feedback schema
│ │ ├── services/ # Logic isolation
│ │ │ ├── llm_service.py # Gemini/OpenAI interface
│ │ │ ├── coach_service.py # Interviewer orchestration
│ │ │ └── judge_service.py # STAR analysis logic
│ │ ├── utils/
│ │ │ ├── pdf_parser.py # PyMuPDF implementation
│ │ │ └── audio_handler.py # Audio conversion logic
│ │ └── main.py # FastAPI entry point
│ ├── pyproject.toml
│ ├── uv.lock
│ ├── .env
│ └── Dockerfile
├── frontend/
│ ├── src/
│ │ ├── assets/ # Styles, images, SVGs
│ │ ├── components/
│ │ │ ├── chat/ # ChatWindow, Bubbles, InputArea
│ │ │ ├── feedback/ # StarMeter, AnalysisCard
│ │ │ └── shared/ # Layout, Uploader, Spinner
│ │ ├── context/ # InterviewContext (Global state)
│ │ ├── hooks/ # useRecorder.js, useInterview.js
│ │ ├── services/ # Axios/api.js instance
│ │ ├── views/ # SetupPage, InterviewPage, Dashboard
│ │ ├── App.jsx
│ │ └── main.jsx
│ ├── tailwind.config.js
│ ├── package.json
│ ├── pnpm-lock.yaml
│ └── Dockerfile
├── compose.ysml # Services: api, ui, db
└── .gitignore
```
