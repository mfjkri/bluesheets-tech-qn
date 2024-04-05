from prisma.models import Item

def sum_items(items: list[Item]) -> float:
    total_spent = 0
    for item in items:
        item_total_price = 0
        if item.total is not None:
            item_total_price = item.total
        elif item.unitPrice is not None and item.quantity is not None:
            item_total_price = item.unitPrice * item.quantity
        
        if item.tax is not None:
            item_total_price += item.tax
            
        total_spent += item_total_price
        
    return round(total_spent, 2)

async def get_item_total_spent_by_tag(item_tag: str) -> float:
    items: list[Item] = await Item.prisma().find_many(where={"itemTag": item_tag})
    return sum_items(items)

async def get_item_total_spent_by_desc(item_desc: str) -> float:
    items: list[Item] = await Item.prisma().find_many(where={"description": item_desc})
    return sum_items(items)