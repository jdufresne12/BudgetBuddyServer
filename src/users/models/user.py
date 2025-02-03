from datetime import datetime
from typing import Optional

class User:
    def __init__(self, user_id: int, first_name: str, last_name: str, email: str, password_hash: str,
                 created_at: datetime, updated_at: datetime, last_login: datetime):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_login = last_login