from uuid import uuid4
from database.db_dep import get_db
from gen_ai.graph import graph_obj
from fastapi import APIRouter, Depends, Request
from database.dbconn import AsyncSession
from core.auth import JWTBearer
from model.context import QAState
from model.my_users import User
from service.get_current_user import get_current_user
from core.rate_limit import limiter
graph = APIRouter(prefix="/graph", tags=["Graph ASK"])

@graph.post("/invoke")
@limiter.limit("2/minute")
async def invoke_graph_a(request:Request ,requests: str, chatid :str , token: str = Depends(JWTBearer()) ,db:AsyncSession = Depends(get_db)):
    user:User=await get_current_user(token=token , db= db)
    result =  await graph_obj.ainvoke(
        QAState(
            user_role= user.role,
            user_id= user.id,
            chat_id= chatid,
            authorized= True,
            question= requests,
            db=db,
            )
    )
    # print(result)
    # logger.info(f"""Query: {request.query} and genrated Response {result["final_answer"]} """)
    
    return {
    "answer": result.get("final_answer") or result.get("answer")
    }