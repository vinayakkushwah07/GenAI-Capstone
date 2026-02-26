from sqlalchemy.ext.asyncio import AsyncSession
from core.password import secure_pwd
from model.my_users import User
from model.token_model import Token
from pydantic import EmailStr
from schemas.main_user_schema import CreateUser
from sqlalchemy import select


async def get_user_by_id(user_id: int, db: AsyncSession):
    """
    Get a user by ID
    """
    try:
        
     result = await db.execute(select(User).where(User.id == user_id).with_for_update())
     await db.commit()
    except Exception:
        pass
    ans = result.first()[0]
    return ans

async def get_user(db: AsyncSession, email: EmailStr):
    try:

        result = await db.execute(
            select(User).where(User.email == email).with_for_update()
        )
    except Exception:
        print(Exception)
    #    print(result.first())
    #    print(type(result))
    return result.first()

async def create_user(db: AsyncSession, user: CreateUser):
    try:
        h_password = secure_pwd(user.password).decode("utf-8")

        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=h_password,
            role=user.role.value,
        )
            
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    except Exception as e:
        await db.rollback()
        print(f"Failed to create user: {e}")
        raise e

def get_token(db: AsyncSession, token: str):
    return db.query(Token).filter(Token.token == token).first()

def create_token(db: AsyncSession, token: str, user_id: int):
    try:
            
        db_token = Token(token=token, user_id=user_id)
        db.add(db_token)
        db.commit() 
        db.refresh(db_token)
        return db_token
    except Exception as e:
        db.rollback()
        print(f"Failed to create Token: {e}")
        raise e