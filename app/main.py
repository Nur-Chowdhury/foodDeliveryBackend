from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import db
from app.routers import auth, orders, menu

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    if db.is_connected():
        await db.disconnect()

app = FastAPI(
    title="Food Delivery API", # Generic Title
    version="3.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(menu.router) # Register Menu Router
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Food Delivery API"}