from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():#异步函数
    return {"message": "Hello World"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


"""比如要使用 /users/me 获取当前用户的数据。

然后还要使用 /users/{user_id}，通过用户 ID 获取指定用户的数据。

由于路径操作是按顺序依次运行的，因此，一定要在 /users/{user_id} 之前声明 /users/me ："""
# @app.post()
# @app.put()
# @app.delete()