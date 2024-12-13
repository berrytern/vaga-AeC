from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import event
from sqlalchemy.orm import Session, sessionmaker
from .schemas import Base
from src.utils import settings
from asyncio import sleep


engine = create_async_engine(settings.POSTGRES_URL)


sync_maker = sessionmaker()
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    sync_session_class=sync_maker,
)


# Register event listener for before_commit, it is a temporary approach, the async event listener is not supported yet
@event.listens_for(Session, "before_commit")
def my_before_commit(session):
    # sync style API use on Session
    # connection = session.connection()
    """print("session.new:", session.new, dir(session), dict(session), flush=True)
    for obj in session.new:
        print("obj:", obj, flush=True)
        if isinstance(obj, FavoriteBookSchema):
            session.execute(
                update(ReaderSchema)
                .where(ReaderSchema.id == obj.reader_id)
                .values(books_read_count=ReaderSchema.books_read_count + 1)
            )"""

    # print("before commit!2", connection, flush=True)


def get_db() -> AsyncSession:
    return SessionLocal()


async def init_models():

    if settings.ENVIRONMENT != "production":
        async with engine.begin() as conn:
            retry = 5
            for try_count in range(1, retry + 1):
                try:
                    async with engine.begin() as conn:
                        await conn.run_sync(Base.metadata.create_all)
                    break
                except BaseException:
                    await sleep(try_count**2)
