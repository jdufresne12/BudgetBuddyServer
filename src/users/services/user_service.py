from typing import List, Optional
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ...utils.password import hash_password
import psycopg2 
from psycopg2.extras import RealDictCursor
import os

class UserService:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")

    async def create_user( self, user_data: UserCreate ) -> Optional[User]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            hashed_password = hash_password(user_data.password)
            
            query = """
                INSERT INTO users (username, email, first_name, last_name, password_hash)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING user_id, username, email, first_name, last_name, password_hash, created_at, updated_at, last_login
            """
            
            cur.execute(query, (
                user_data.username,
                user_data.email,
                user_data.first_name,
                user_data.last_name,
                hashed_password
            ))
            user_record = cur.fetchone()
            conn.commit()
            
            if user_record:
                return User(**user_record)
            
            return None
            
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            raise
        finally:
            cur.close()
            conn.close()

    async def delete_user( self, user_id: int ) -> Optional[User]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                DELETE FROM users 
                WHERE user_id = %s
                RETURNING user_id, username, email, first_name, last_name, password_hash, created_at, updated_at, last_login
            """
            
            cur.execute(query, (user_id,))
            user_record = cur.fetchone()
            conn.commit()
            
            if user_record:
                return User(**user_record)
            
            return None
            
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            raise
        finally:
            cur.close()
            conn.close()

    async def get_all_users( self ) -> List[User]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """ SELECT * FROM users """
            
            cur.execute(query)
            user_records = cur.fetchall()
            
            users = [User(**record) for record in user_records]
            
            return users
            
        except Exception as e:
            print(f"Error getting all users: {str(e)}")
            raise
        finally:
            cur.close()
            conn.close()

    async def get_user(self, user_id: int) -> Optional[User]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT * FROM users
                WHERE user_id = %s
            """
            
            cur.execute(query, (user_id,))
            user_record = cur.fetchone()
            
            if user_record:
                return User(**user_record)
            
            return None
            
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            raise
        finally:
            cur.close()
            conn.close()

        