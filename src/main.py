from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
from prisma import Prisma

from src.prisma.prisma import (
    get_item_total_spent_by_desc, 
    get_item_total_spent_by_tag
)

load_dotenv()
app = FastAPI()
db = Prisma(auto_register=True)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get('/whoami', response_class=PlainTextResponse)
async def whoami() -> str:
    return "Bluesheets Warehouse API"

@app.get('/total_spent_on_item_by_tag')
async def total_spent_on_item_by_tag(item_tag: str = Query(..., title="Item Tag")):
    total_spent = await get_item_total_spent_by_tag(item_tag)
    return {"item_tag": item_tag, "total_spent": total_spent}

@app.get('/total_spent_on_item_by_desc')
async def total_spent_on_item_by_desc(item_desc: str = Query(..., title="Item Description")):
    total_spent = await get_item_total_spent_by_desc(item_desc)
    return {"item_desc": item_desc, "total_spent": total_spent}