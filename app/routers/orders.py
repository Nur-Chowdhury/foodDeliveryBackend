from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated, List
from app import schemas
from app.database import db
from app.security import get_current_user, get_current_admin
from prisma.models import User

router = APIRouter(prefix="/orders", tags=["Orders"])

UserDep = Annotated[User, Depends(get_current_user)]
AdminDep = Annotated[User, Depends(get_current_admin)]

@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(order: schemas.OrderCreate, user: UserDep):
    # 1. Fetch the food item to get the price
    food_item = await db.fooditem.find_unique(where={"id": order.food_item_id})
    
    if not food_item or not food_item.is_active:
        raise HTTPException(status_code=404, detail="Food item not found or unavailable")

    # 2. Calculate Total Price
    total_price = food_item.price * order.quantity

    # 3. Create Order
    new_order = await db.order.create(
        data={
            "quantity": order.quantity,
            "total_price": total_price,
            "status": "PENDING",
            "user_id": user.id,
            "food_item_id": food_item.id
        },
        include={"food_item": True} # Include details for response
    )
    return new_order

@router.get("/", response_model=List[schemas.OrderResponse])
async def list_all_orders(admin: AdminDep):
    """Admin: View all orders in the system"""
    return await db.order.find_many(include={"food_item": True})

@router.get("/me", response_model=List[schemas.OrderResponse])
async def get_my_orders(user: UserDep):
    """User: View my own orders"""
    return await db.order.find_many(
        where={"user_id": user.id},
        include={"food_item": True}
    )

@router.get("/{order_id}", response_model=schemas.OrderResponse)
async def get_order_detail(order_id: int, user: UserDep):
    """Get details of a specific order (User can only see their own)"""
    order = await db.order.find_unique(
        where={"id": order_id},
        include={"food_item": True}
    )
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    # Check permission: Admin OR Owner
    if not user.is_staff and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    return order

@router.put("/status/{order_id}", response_model=schemas.OrderResponse)
async def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, admin: AdminDep):
    """Admin: Update order status"""
    try:
        return await db.order.update(
            where={"id": order_id},
            data={"status": status_update.status},
            include={"food_item": True}
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Order not found")