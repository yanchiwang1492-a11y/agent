from fastapi import FastAPI
from contextlib import asynccontextmanager
from demo.email_agent import EmailAgent
import uvicorn

@asynccontextmanager
async def test(app:FastAPI):
    app.state.email_agent = EmailAgent()
    print("EmailAgent实例化成功")
    yield
    app.state.email_agent = None
    print("EmailAgent实例消耗")
app = FastAPI(lifespan=test)

if __name__=="__main__":
   uvicorn.run(app,host="localhost",port=8000)