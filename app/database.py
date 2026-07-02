from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:test@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# to create a new session for each request, we can define a dependency function that creates a new session and yields it, and then we can use the Depends function from FastAPI to inject the session into our route handlers, like this:


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
