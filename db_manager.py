import os
import logging
from sqlalchemy import create_url, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Configure Logging for a Senior-level project
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class DatabaseManager:
    """
    Handles connections to the PostgreSQL/pgvector metadata store.
    Designed for scalability and robust error handling.
    """
    
    def __init__(self):
        # Defaulting to environment variables (Standard for AI/DevOps)
        self.db_user = os.getenv("DB_USER", "admin")
        self.db_pass = os.getenv("DB_PASS", "password")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_name = os.getenv("DB_NAME", "rag_metadata")
        self.engine = self._get_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _get_engine(self):
        """Creates a SQLAlchemy engine with connection pooling."""
        try:
            url = f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}"
            return create_engine(
                url, 
                pool_size=10, 
                max_overflow=20,
                pool_pre_ping=True
            )
        except Exception as e:
            logger.error(f"Failed to create engine: {e}")
            raise

    def get_session(self):
        """Dependency for FastAPI or standalone scripts to handle DB sessions."""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def check_health(self):
        """Verifies connection to the database (used for API health checks)."""
        try:
            with self.engine.connect() as conn:
                logger.info("Successfully connected to the database.")
                return True
        except SQLAlchemyError as e:
            logger.error(f"Database health check failed: {e}")
            return False

if __name__ == "__main__":
    # Test block for local execution
    manager = DatabaseManager()
    manager.check_health()
