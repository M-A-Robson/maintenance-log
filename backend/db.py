import asyncio
import aiosqlite


async def create_table(statement: str, db_path: str) -> None:
    async with aiosqlite.connect(db_path) as db:
        await db.execute(statement)
        await db.commit()


async def main() -> None:
    async with asyncio.TaskGroup() as tasks:
        tasks.create_task(
            create_table(
                '''CREATE TABLE IF NOT EXISTS todos (
                    id INT NOT NULL,
                    note TEXT,
                    PRIMARY KEY (ID)
                    )''', "todo.db"
            )
        )
        
if __name__ == "__main__":
    asyncio.run(main())