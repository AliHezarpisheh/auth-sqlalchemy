"""Custom fixtures and configurations for pytest tests."""

from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add custom command line option for pytest.

    Parameters
    ----------
    parser : pytest.Parser
        The pytest parser object.
    """
    parser.addoption(
        "--dburl",
        action="store",
        default=(
            "postgresql+psycopg2://postgres:postgres@localhost"
            "/test_auth_db_sample_project"
        ),
        help="URL of the database, used for tests",
    )


@pytest.fixture(scope="session")
def db_url(request: pytest.FixtureRequest) -> str:
    """
    Fixture to retrieve the database URL from pytest command line options.

    Parameters
    ----------
    request : pytest.FixtureRequest
        The request object for accessing pytest configurations.

    Returns
    -------
    str
        The database URL.
    """
    database_url: str = request.config.getoption("--dburl")
    return database_url


@pytest.fixture(scope="session")
def db_engine(db_url: str) -> Generator[Engine, None, None]:
    """
    Fixture providing a SQLAlchemy engine instance connected to the database.

    Parameters
    ----------
    db_url : str
        The URL of the database.

    Yields
    ------
    Generator[Engine, None, None]
        A generator yielding the SQLAlchemy engine instance.
    """
    engine = create_engine(db_url, echo=True)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine: Engine) -> scoped_session[Session]:
    """
    Fixture providing a factory for scoped SQLAlchemy sessions.

    Parameters
    ----------
    db_engine : Engine
        The SQLAlchemy engine instance.

    Returns
    -------
    scoped_session[Session]
        A scoped SQLAlchemy session factory.
    """
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(
    db_session_factory: scoped_session[Session],
) -> Generator[Session, None, None]:
    """
    Fixture providing a factory for scoped SQLAlchemy sessions.

    Parameters
    ----------
    db_engine : Engine
        The SQLAlchemy engine instance.

    Returns
    -------
    scoped_session[Session]
        A scoped SQLAlchemy session factory.
    """
    session = db_session_factory()
    yield session
    session.rollback()
    session.close()
