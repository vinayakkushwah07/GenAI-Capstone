
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_dep import get_db
from service.user_crud import  get_user ,create_user,get_user_by_id
from core.password import verify_pwd
from core.auth import  create_access_token, create_refresh_token,decodeJWT ,JWTBearer
from schemas.main_user_schema import LoginUser,CreateUser, PostUser
from datetime import  timedelta
from fastapi.security import OAuth2PasswordBearer


auth_route = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2bearer = OAuth2PasswordBearer(tokenUrl = 'auth/login')



@auth_route.get("/getuser")
async def get_current_user(token: str = Depends(JWTBearer()) ,db:AsyncSession = Depends(get_db)) :
    """
    Get current user from JWT token
    """
    payload = decodeJWT(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )
    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )
    print(type(user_id), f"value {user_id}") 
    user = await get_user_by_id(user_id ,db= db)
     
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@auth_route.post("/register")
async def register_user(payload: CreateUser, db: AsyncSession = Depends(get_db)):
    
    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please add Email",
        )
    
    user = await get_user(db, payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {payload.email} already exists",
        )
    
    user = await create_user(db, payload)
    print(user)
    user_r = PostUser.model_validate(user)
    return user_r


@auth_route.post("/login")
async def login_user(payload: LoginUser, db: AsyncSession = Depends(get_db)):
    """
    Login user based on email and password
    """
    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please add Phone number",
        )
    
    user = await get_user(db, payload.email)
    user = user[0]
    
    # print(user)
    # print(type(user))
    
    if verify_pwd( payload.password ,user.hashed_password.encode(encoding="utf-8") ):

        token =  create_access_token(user.id, timedelta(minutes=30)) 
        refresh = create_refresh_token(user.id,timedelta(minutes = 1008))

        return {'access_token': token, 'token_type': 'bearer','refresh_token':refresh,"user_id":user.id}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Password Or  Email   is Incorrect ",
        )