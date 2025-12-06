from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated, List
from app import schemas
from app.database import db
from app.security import get_current_user, get_current_admin
from prisma.models import User

router = APIRouter(prefix="/menu", tags=["Menu"])

UserDep = Annotated[User, Depends(get_current_user)]
AdminDep = Annotated[User, Depends(get_current_admin)]

@router.get("/", response_model=List[schemas.FoodItemResponse])
async def get_menu():
    """List all active food items"""
    return await db.fooditem.find_many(where={"is_active": True})

@router.post("/", response_model=schemas.FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def add_food_item(item: schemas.FoodItemCreate, admin: AdminDep):
    """Admin only: Add a new item to the menu"""
    new_item = await db.fooditem.create(
        data={
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "category": item.category,
            "is_active": item.is_active
        }
    )
    return new_item

@router.put("/{item_id}", response_model=schemas.FoodItemResponse)
async def update_food_item(item_id: int, item: schemas.FoodItemCreate, admin: AdminDep):
    """Admin only: Update a menu item"""
    updated = await db.fooditem.update(
        where={"id": item_id},
        data={
            "name": item.name,
            "price": item.price,
            "category": item.category,
            "is_active": item.is_active
        }
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated