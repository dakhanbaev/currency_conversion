# pylint: disable=redefined-outer-name
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from adapters.orm import metadata, start_mappers

pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
def mapper():
    start_mappers()


@pytest_asyncio.fixture(scope="session")
async def in_memory_sqlite_db():
    return create_async_engine("sqlite+aiosqlite:///:memory:")


@pytest_asyncio.fixture
async def create_db(in_memory_sqlite_db):
    async with in_memory_sqlite_db.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with in_memory_sqlite_db.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db, create_db):
    yield sessionmaker(bind=in_memory_sqlite_db, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture
def session(sqlite_session_factory):
    return sqlite_session_factory()
