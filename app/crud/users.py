from fastapi import Depends, HTTPException
from app.schemas.users import UserCreate, Login
from app.db.auth import get_supabase
from datetime import datetime, timedelta
from app.core.security import create_access_token
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
        # print(type(response))
        # print(response.data)
        user_id=response.user.id
        # print(dict(response).get("user"))
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=access_token_expires
        )
        return {"message": "User logged in successfully", "access_token": access_token}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
