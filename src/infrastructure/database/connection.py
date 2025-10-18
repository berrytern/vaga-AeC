from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.utils.settings import POSTGRES_URL

engine = create_async_engine(POSTGRES_URL, echo=False)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


def get_session() -> AsyncSession:
    """Create and return a new assynchronous session"""
    return SessionLocal()
