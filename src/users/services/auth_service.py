from typing import List, Optional
from ..models.user import User
from ..schemas.auth import LoginRequest, LoginResponse
from ...utils.password import verify_password
from ...utils.auth_token import create_access_token
import psycopg2 
from psycopg2.extras import RealDictCursor
import os

class AuthService:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
    
    async def login( self, user_data: LoginRequest ):
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """SELECT * from users WHERE username = %s"""
            
            cur.execute(query, (user_data.username,))
            user_record = cur.fetchone()
            
            if user_record and verify_password(user_data.password, user_record['password_hash']):
                user = User(**user_record)
                token_data = {
                    "sub": user.username,
                    "user_id": user.user_id,
                    "email": user.email
                }
                access_token = create_access_token(token_data)               

                return user, access_token
            
            return None, None
            
        except Exception as e:
            print(f"Login Error: {str(e)}")
            raise
        finally:
            cur.close()
            conn.close()