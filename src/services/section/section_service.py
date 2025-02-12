from typing import List, Optional
from ...schemas.section import CreateSectionData, CreateSectionResponse, DeleteSectionData, GetMonthsSectionsData
import psycopg2  # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
import os

class SectionService:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")

    async def create_section( self, data: CreateSectionData ) -> Optional[CreateSectionResponse]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                INSERT INTO budget_sections (user_id, name, start_date, end_date)
                VALUES (%s, %s, %s, %s)
                RETURNING section_id, name, start_date, end_date
            """

            cur.execute(query, (
                data.user_id,
                data.name, 
                str(data.start_date),
                str(data.end_date) if data.end_date is not None else None
            ))
            response = cur.fetchone()
            conn.commit()

            if response:
                return CreateSectionResponse(**response)
            
            return None
        
        except Exception as e:
            print(f'Error creating section: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()

    async def get_months_sections( self, data: GetMonthsSectionsData ) -> Optional[List[CreateSectionResponse]]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                SELECT section_id, name, start_date, end_date
                FROM budget_sections
                WHERE user_id = %s
                AND EXTRACT(MONTH FROM start_date) <= %s + 1
                AND (end_date IS NULL) or (EXTRACT(MONTH FROM end_date) = %s + 1)
                AND EXTRACT(YEAR FROM start_date) = %s;
            """ 

            cur.execute(query, (
                data.user_id,
                data.month,
                data.month,
                data.year
            ))
            response = cur.fetchall()

            # Convert each row to a CreateSectionResponse object and return a list
            return [CreateSectionResponse(**row) for row in response] if response else []

        except Exception as e:
            print(f'Error getting sections for this month: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()

    async def delete_section( self, data: DeleteSectionData) -> bool:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                DELETE FROM budget_sections
                WHERE user_id = %s AND section_id = %s
                RETURNING section_id
            """

            cur.execute(query, (
                data.user_id, 
                data.section_id
            ))
            deleted = cur.fetchone()
            conn.commit()

            return bool(deleted)

        except Exception as e:
            print(f'Error deleting section: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()
            

