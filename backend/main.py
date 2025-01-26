from fastapi import FastAPI, status
import aiosqlite
from typing import Any
from schemas import ToDo


app = FastAPI()

@app.get('/')
async def home():
    return {'message':'hello world'}

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(data:ToDo):
    async with aiosqlite.connect("todo.db") as conn:
        await conn.execute(
            "INSERT INTO todos (id,note) VALUES (?,?)",
            (data.id, data.note),
        )
        await conn.commit()
    return "todo created"

@app.get("/todo/{id}")
async def read_todo(id:int):
    async with aiosqlite.connect("todo.db") as conn:
        async with conn.execute("SELECT * FROM todos WHERE id = ?", (id,)) as cursor:
            todo = await cursor.fetchall()
    return {"todo": todo}

@app.put("/todo/{id}")
async def update_todo(id:int, note: str):
    async with aiosqlite.connect("todo.db") as conn:
        await conn.execute('''UPDATE todos
                            SET note = ?
                            WHERE id = ?''', (note, id))
        await conn.commit()
    return f"todo {id} updated"

@app.delete("/todo/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_todo(id:int):
    async with aiosqlite.connect("todo.db") as conn:
        await conn.execute("DELETE FROM todos WHERE id = ?", (id,))
        await conn.commit()
    return f"todo {id} deleted"

@app.get("/todo")
async def get_todos():
    async with aiosqlite.connect("todo.db") as conn:
        async with conn.execute("SELECT * FROM todos") as cursor:
            todos = await cursor.fetchall()
    return {"todos": todos}

