from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from datetime import datetime, timedelta
from typing import Optional
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # print(JWT_SECRET_KEY)
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    # print(encoded_jwt)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        # print("payload: ",payload)
        # print("email: ",email)
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(verify_token)):
    return token
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         # Decode the JWT token using your secret key and algorithm.
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="User not found",
#             )
#         # Return a dictionary with the user's id (you can add more user info if needed)
#         return {"user_id": user_id}
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#         )