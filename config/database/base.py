"""Module for defining base database configurations."""

from configparser import ConfigParser

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class DatabaseConnection:
    """Class for managing database connections."""

    def __init__(self, config_path: str = "alembic.ini") -> None:
        """
        Initialize DatabaseConnection with the specified configuration path.

        Parameters
        ----------
        config_path : str, optional
            Path to the configuration file. Defaults to "alembic.ini".
        """
        self._config_path = config_path
        self._engine: Engine | None = None

    def get_engine(self) -> Engine:
        """
        Get the database engine.

        Returns
        -------
        sqlalchemy.engine.Engine
            The database engine object.
        """
        if not self._engine:
            config = self._load_alembic_config()
            db_url = config.get("alembic", "sqlalchemy.url")
            self._engine = create_engine(db_url)
        return self._engine

    def _load_alembic_config(self) -> ConfigParser:
        """
        Load the Alembic configuration file.

        Returns
        -------
        configparser.ConfigParser
            A ConfigParser object containing the Alembic configuration.
        """
        parser = ConfigParser()
        parser.read(self._config_path)
        return parser

    def get_session(self) -> scoped_session[Session]:
        """
        Get a scoped database session.

        Returns
        -------
        sqlalchemy.orm.scoped_session[Session]
            A scoped session object.
        """
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        return scoped_session(Session)
