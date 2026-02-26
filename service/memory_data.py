from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from model.chat_model import ChatMessage

async def save_message_to_db(
    db: AsyncSession,
    user_id: int,
    chat_id: str,
    role: str,
    content: str,
):
    # print("\n \n ------------------- this is save chat ---------------")
    # print(user_id)
    # print(chat_id)
    
    stmt = insert(ChatMessage).values(
        user_id=user_id,
        chat_id=chat_id,
        role=role,
        content=content
    )

    await db.execute(stmt)
    await db.commit()
    
    
async def get_last_n_messages(
    db: AsyncSession,
    user_id: int,
    chat_id: str,
    limit: int = 5
):
    # print("\n \n ------------------- this is retrive chat ---------------")
    
    # print(chat_id)
    # print(user_id)
    stmt = (
        select(ChatMessage)
        .where(
            ChatMessage.user_id == user_id,
            ChatMessage.chat_id == chat_id
        )
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()

    rows = list(reversed(rows))

    print(rows)
    return [
        {"role": row.role, "content": row.content}
        for row in rows
    ]
    
