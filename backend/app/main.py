from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import uploads, interviews, feedback
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    uploads.router, prefix=f"{settings.API_V1_STR}/uploads", tags=["uploads"]
)
app.include_router(
    interviews.router, prefix=f"{settings.API_V1_STR}/interview", tags=["interview"]
)
app.include_router(
    feedback.router, prefix=f"{settings.API_V1_STR}/feedback", tags=["feedback"]
)


@app.get("/")
def root():
    return {"message": "Karamazov AI API is online"}
