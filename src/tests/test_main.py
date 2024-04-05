import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from test_utils import MockItem
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_whoami(client):
    response = client.get("/whoami")
    assert response.status_code == 200
    assert response.text == "Bluesheets Warehouse API"

@pytest.mark.asyncio
async def test_total_spent_on_item_by_tag(client):
    mock_prisma = AsyncMock()
    mock_prisma.find_many.return_value = [MockItem(total=20), MockItem(total=30)]
    with patch("src.prisma.prisma.Item.prisma", return_value=mock_prisma):
        response = client.get("/total_spent_on_item_by_tag?item_tag=ITEM_TAG")
        assert response.status_code == 200
        assert "item_tag" in response.json()
        assert "total_spent" in response.json()
        assert response.json()["total_spent"] == 50

@pytest.mark.asyncio
async def test_total_spent_on_item_by_desc(client):
    mock_prisma = AsyncMock()
    mock_prisma.find_many.return_value = [MockItem(total=40), MockItem(total=20)]
    with patch("src.prisma.prisma.Item.prisma", return_value=mock_prisma):
        response = client.get("/total_spent_on_item_by_desc?item_desc=ITEM_DESC")
        assert response.status_code == 200
        assert "item_desc" in response.json()
        assert "total_spent" in response.json()
        assert response.json()["total_spent"] == 60
