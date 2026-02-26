from fastapi import HTTPException ,status
from core.auth import decodeJWT
from model.my_users import User
from service.user_crud import get_user_by_id


async def get_current_user(token , db) -> User :
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