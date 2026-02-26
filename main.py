from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from model.my_users import AppUser,User,Chat
from model.chat_model import ChatMessage
from database.dbconn import Base,engine
from api.v1.auth_endpoint import auth_route
from api.v1.rag_upload_endpoint import rag_upload
from api.v1.graph_endpoint import graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)


app.include_router(auth_route)
app.include_router(rag_upload)
app.include_router(graph)



import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
