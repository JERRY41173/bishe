from fastapi import Depends, FastAPI
import uvicorn
# from .dependencies import get_query_token, get_token_header
# from .internal import admin
from routers import items, users ,writer,solutions

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(writer.router)
app.include_router(solutions.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == '__main__':
    uvicorn.run('main:app')