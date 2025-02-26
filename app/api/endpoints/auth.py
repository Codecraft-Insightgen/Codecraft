from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends
from app.schemas.users import UserCreate, Login
from app.db.auth import get_supabase
from app.crud.users import create_user, login

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/signup")
async def create_user_endpoint(user: UserCreate, db=Depends(get_supabase)):
    return await create_user(user, db)

@router.post("/login")
async def login_endpoint(user: Login, db=Depends(get_supabase)):
    return await login(user, db)