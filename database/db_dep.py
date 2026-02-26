from database.dbconn import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db():
    db =  AsyncSessionLocal()
    
    try:
        yield  db
    finally:
       await db.close()
# AsyncSession