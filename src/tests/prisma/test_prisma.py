import pytest
from unittest.mock import AsyncMock, patch

from src.tests.test_utils import MockItem
from src.prisma.prisma import (
    sum_items, get_item_total_spent_by_tag, get_item_total_spent_by_desc
)

SAMPLE_TOTAL = 86

@pytest.fixture
def sample_items():
    return [
        MockItem(total=10),
        MockItem(unitPrice=5, quantity=2),
        MockItem(total=20, tax=3),
        MockItem(unitPrice=5, quantity=4, tax=3),
        MockItem(unitPrice=5, quantity=2, total=20),
    ]

def test_sum_items(sample_items):
    total_spent = sum_items(sample_items)
    assert total_spent == SAMPLE_TOTAL

@pytest.mark.asyncio
async def test_get_item_total_spent_by_tag(sample_items):
    mock_prisma = AsyncMock()
    mock_prisma.find_many.return_value = sample_items
    with patch("src.prisma.prisma.Item.prisma", return_value=mock_prisma):
        total_spent = await get_item_total_spent_by_tag("ITEM_TAG")
        assert total_spent == SAMPLE_TOTAL

@pytest.mark.asyncio
async def test_get_item_total_spent_by_desc(sample_items):
    mock_prisma = AsyncMock()
    mock_prisma.find_many.return_value = sample_items
    with patch("src.prisma.prisma.Item.prisma", return_value=mock_prisma):
        total_spent = await get_item_total_spent_by_desc("ITEM_DESC")
        assert total_spent == SAMPLE_TOTAL
