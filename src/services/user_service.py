from ..utils.database import Database

class UserService:
   async def create_user(self, username: str, email: str, password: str):
       pool = await Database.connect()
       async with pool.acquire() as conn:
           query = """
            INSERT INTO users (username, email, password_hash)
            VALUES ($1, $2, $3)
            RETURNING id, username, email
           """
           return await conn.fetchrow(query, username, email, password)