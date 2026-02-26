from os import access
from typing import List, Literal, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request , UploadFile , status ,File

from core.auth import JWTBearer, decodeJWT
from data_pipeline.add_to_vdb import  get_rag_data_vdb
from data_pipeline.file_pre_proc import upload_file
from database.db_dep import get_db
from database.dbconn import AsyncSession
from model.my_users import User
from schemas.access_role import AccesRole
from service.get_current_user import get_current_user
from core.rate_limit import limiter

rag_upload = APIRouter(prefix="/rag", tags=["RAG UPLOAD"])

@rag_upload.post("/upload")    
@limiter.limit("2/minute")
async def upload_file_a( 
        request:Request ,
        # access_role: List[str] = Form(...),
        access_role: Optional[List[AccesRole]] = Query(None, description="Select multiple Roles"),
        file: UploadFile = File(...), 
        token: str = Depends(JWTBearer()),
        
    ):
    print("acess role :- ",access_role,"its types :- ",type(access_role))
    payload = decodeJWT(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )
    user_id = int(payload.get("sub"))
    return await upload_file(
        file=file,
        allowed_role= access_role,
        uploaded_by= user_id
    )
    
@rag_upload.get("/query")   
@limiter.limit("5/minute")
async def run( request:Request ,query:str , token: str = Depends(JWTBearer()) ,db:AsyncSession = Depends(get_db)):
    user:User=await get_current_user(token=token , db= db)
    response = await get_rag_data_vdb(query=query , role = user.role)
    return {"data": response}
    