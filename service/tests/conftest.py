from httpx import AsyncClient, ASGITransport 
from service.app import app
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
import pytest_asyncio

@pytest_asyncio.fixture(scope="session")
async def test_app():
    async with LifespanManager(app):
        yield app  # testing happens here
        
        
@pytest_asyncio.fixture(scope='session')
async def test_client(test_app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url='http://localhost') as client:
        yield client