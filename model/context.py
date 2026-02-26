from typing import Dict, List, Optional, TypedDict
from pydantic import BaseModel, ConfigDict
from langchain_core.documents import Document
from database.dbconn import AsyncSession

class QAState(BaseModel):
    question: str
    query_type: Optional[str] = None
    chat_summary: Optional[str] = None
    msg_history: Optional[List[dict]] = None
    documents: Optional[List[Document]] = None
    answer: Optional[str] = None
    validation_passed: Optional[bool] = None
    final_answer: Optional[str] = None
    rang_tool: Optional[str] = None
    user_role: Optional[str] = None
    masked_data: Optional[Dict] = None
    user_id: int
    chat_id: str
    authorized: Optional[bool] = None
    db: Optional[AsyncSession] = None
    is_safe:Optional[bool] = True
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    
    
 