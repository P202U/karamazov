from sqlmodel import create_engine
from app.core.config import settings

# The engine handles the connection pool to Postgres
engine = create_engine(settings.DATABASE_URL, echo=True)
