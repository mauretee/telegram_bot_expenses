import logging
import pytest
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from app.database import POSTGRES_DB, POSTGRES_PASSWORD, Base
from app.utils import get_env_variable
from app.main import app
from app.models import User
from app.database import get_db
from fastapi.testclient import TestClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


POSTGRES_DB: str = get_env_variable("POSTGRES_DB")
POSTGRES_USER: str = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD: str = get_env_variable("POSTGRES_PASSWORD")
DB_HOST: str = get_env_variable("DB_HOST")
DB_PORT: str = get_env_variable("DB_PORT")

# Set up a test database URL
TEST_SQLALCHEMY_DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/test_db"
POSTGRESQL_ADMIN_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

admin_engine = create_engine(
   POSTGRESQL_ADMIN_DATABASE_URI, isolation_level="AUTOCOMMIT"
)

# Create an engine and sessionmaker bound to the test database
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_database():
    """Create the test database if it doesn't exist."""
    with admin_engine.connect() as connection:
        try:
            connection.execute(
                text(f"CREATE DATABASE {TEST_SQLALCHEMY_DATABASE_URL.split('/')[-1]}")
            )
            logger.info("Test database created successfully.")
        except ProgrammingError:
            logger.info("Database already exists, continuing...")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    logger.info("Setting up test database...")
    create_test_database()  # Ensure the test database is created
    Base.metadata.create_all(bind=engine)  # Create tables
    logger.info("Test database schema created.")
    yield
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests
    logger.info("Test database schema dropped.")


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Create a new database session for each test and roll it back after the test.
    """
    logger.info("Creating a new database session for the test...")
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    logger.info("Database session closed and transaction rolled back.")


@pytest.fixture()
def client(db):

    def override_get_db():
        try:

            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture(scope="function")
def user(db):
    new_user = User(telegram_id=1)
    db.add(new_user)
    db.commit()
