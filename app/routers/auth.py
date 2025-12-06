from fastapi import APIRouter, status, HTTPException
from app import schemas
from app.database import db
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=schemas.UserData, status_code=status.HTTP_201_CREATED)
async def signup(user: schemas.SignUpModel):
    existing = await db.user.find_first(
        where={"OR": [{"email": user.email}, {"username": user.username}]}
    )
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = await db.user.create(
        data={
            "username": user.username,
            "email": user.email,
            "password": get_password_hash(user.password),
            "is_staff": user.is_staff,
            "is_active": user.is_active
        }
    )
    return new_user

@router.post("/login", response_model=schemas.Token)
async def login(creds: schemas.LoginModel):
    user = await db.user.find_unique(where={"username": creds.username})
    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}