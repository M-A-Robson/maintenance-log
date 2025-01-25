from fastapi import FastAPI, status
import aiosqlite
from typing import Any


app = FastAPI()

@app.get('/')
async def home():
    return {'message':'hello world'}

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(data: dict[str, Any]):
    async with aiosqlite.connect("todo.db") as conn:
        await conn.execute(
            "INSERT INTO todos (id,note) VALUES (?,?)",
            (data["id"], data["note"]),
        )
        await conn.commit()
    return "todo created"

# @app.get("/todo/{id}")
# def read_todo(id: int):
#     return "read todo item with id {id}"

# @app.put("/todo/{id}")
# def update_todo(id: int):
#     return "update todo item with id {id}"

# @app.delete("/todo/{id}")
# def delete_todo(id: int):
#     return "delete todo item with id {id}"

@app.get("/todo")
async def get_todo():
    async with aiosqlite.connect("todo.db") as conn:
        async with conn.execute("SELECT * FROM todos") as cursor:
            todos = await cursor.fetchall()
    return {"todos": todos}

