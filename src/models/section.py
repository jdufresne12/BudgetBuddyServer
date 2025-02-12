from datetime import datetime

class Section:
    def __init__(self, section_id: int, user_id: int, name: str, start_date: datetime,
            end_date: datetime, created_at: datetime, updated_at: datetime):
        self.section_id = section_id
        self.user_id = user_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.updated_at = updated_at
