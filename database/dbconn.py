from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from core.settings import settings
from sqlalchemy.orm import declarative_base
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, 
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
Base = declarative_base()