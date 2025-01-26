from fastapi import FastAPI, status, HTTPException
import aiosqlite
from schemas import ToDo


app = FastAPI()

@app.get('/')
async def home():
    return {'message':'hello world'}

@app.get("/todo/{id}")
async def read_todo(id:int):
    """Retrieve a single item by id"""
    async with aiosqlite.connect("todo.db") as conn:
        async with conn.execute("SELECT * FROM todos WHERE id = ?", (id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"no todo with id: {id} found in todos")
            return {"todo":row}

@app.get("/todo")
async def get_all_todos():
    """Retrieve all items in database"""
    async with aiosqlite.connect("todo.db") as conn:
        async with conn.execute("SELECT * FROM todos") as cursor:
            todos = await cursor.fetchall()
    return {"todos": todos}

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(data:ToDo):
    """Create a new entry"""
    try:
        async with aiosqlite.connect("todo.db") as conn:
            await conn.execute(
                "INSERT INTO todos (id,note) VALUES (?,?)",
                (data.id, data.note),
            )
            await conn.commit()
        return "todo created"
    except aiosqlite.IntegrityError as e:
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.put("/todo/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(id:int, note: str):
    """Modify an existing database entry"""
    async with aiosqlite.connect("todo.db") as conn:
        async with conn.execute("SELECT EXISTS(SELECT 1 FROM todos WHERE id = ? LIMIT 1)", (id,)) as cursor:
            record = await cursor.fetchone()
            if record[0] == 1:
                await conn.execute('''UPDATE todos
                                    SET note = ?
                                    WHERE id = ?''', (note, id))
                await conn.commit()
                return f"todo {id} updated"
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"no todo with id: {id} found in todos")

@app.delete("/todo/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_todo(id:int):
    """Delete a database entry by id"""
    async with aiosqlite.connect("todo.db") as conn:
        await conn.execute("DELETE FROM todos WHERE id = ?", (id,))
        await conn.commit()
    return f"todo {id} deleted"

@app.get("/id")
async def get_next_id() -> int:
    """Finds the next available integer value that can be used as an id"""
    async with aiosqlite.connect("todo.db") as conn:
        async with conn.execute("SELECT MAX(id) FROM todos") as cursor:
            val = await cursor.fetchone()
            return val[0]+1
    
            

