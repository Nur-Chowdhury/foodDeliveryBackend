from pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum
from typing import Optional

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class SignUpModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_staff: bool = False
    is_active: bool = True

class LoginModel(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserData(BaseModel):
    id: int
    username: str
    email: str
    is_staff: bool
    model_config = ConfigDict(from_attributes=True)

class FoodItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_active: bool = True

class FoodItemResponse(FoodItemCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    food_item_id: int
    quantity: int

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(BaseModel):
    id: int
    quantity: int
    status: OrderStatus
    total_price: float
    user_id: int
    food_item: FoodItemResponse
    
    model_config = ConfigDict(from_attributes=True)