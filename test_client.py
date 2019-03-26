import asyncio
import asyncpg


async def run():
    conn = await asyncpg.connect(user='postgres', password='password', database='postgres', host='127.0.0.1')

    async with conn.transaction():
        await conn.execute(f"DELETE FROM fixtures;")
    for i in range(1000):
        async with conn.transaction():
            await conn.execute(f"INSERT INTO fixtures VALUES({i}, {i})")

        asyncio.sleep(1)
    await conn.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
