from sqlmodel import SQLModel
from app.db.session import engine
from app.models.interview import InterviewSession
from app.models.message import Message


def init_db():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    init_db()
