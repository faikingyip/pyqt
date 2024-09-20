import abc

import psycopg2
from sqlalchemy.ext import asyncio


class AbstractDbManager(abc.ABC):

    def __init__(self):
        self.session_factory: asyncio.async_sessionmaker = None

    @abc.abstractmethod
    def check_conn(self) -> bool:
        raise NotImplementedError()

    # @abc.abstractmethod
    # async def get_session(self):
    #     raise NotImplementedError()


CHECK_CONN_TIMEOUT = 3


class DbManager(AbstractDbManager):
    """Manages connections to the database."""

    instance = None

    @staticmethod
    def get_instance():
        if not DbManager.instance:
            DbManager.instance = DbManager()
        return DbManager.instance

    def __init__(self):
        super().__init__()
        self.db_url: str = None
        self.engine: asyncio.AsyncEngine = None
        # self.session_factory: asyncio.async_sessionmaker = None

        self.db_host: str = None
        self.db_port: str = None
        self.db_name: str = None
        self.db_user: str = None
        self.db_pass: str = None

    def setup(
        self,
        db_host: str,
        db_port: str,
        db_name: str,
        db_user: str,
        db_pass: str,
    ):
        self.db_url = (
            f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

        self.engine = asyncio.create_async_engine(
            self.db_url,
            # echo=True,
        )

        self.session_factory = asyncio.async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

    def check_conn(self) -> bool:
        """Checks the connection to the database.
        Check is performed in sync mode."""

        if not self.db_host:
            return False

        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass,
                connect_timeout=CHECK_CONN_TIMEOUT,
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            return False
        except Exception:
            return False

    # async def get_session(self) -> AsyncSession:
    #     async with self.session_factory() as db:
    #         try:
    #             yield db
    #         finally:
    #             await db.close()
