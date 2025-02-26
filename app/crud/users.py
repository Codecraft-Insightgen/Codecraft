from fastapi import Depends, HTTPException
from app.schemas.users import UserCreate, Login
from app.db.auth import get_supabase

async def create_user(user:UserCreate, db=Depends(get_supabase)):
    try:
        response = db.auth.admin.create_user({
            "email": user.email,
            "username" : user.username,
            "full_name": user.full_name,
            "password": user.password
        })
        return {"message": "User created successfully", "data": response}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


async def login(user: Login, db=Depends(get_supabase)):
    try:
        response = db.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return {"message": "User logged in successfully", "data": response}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
