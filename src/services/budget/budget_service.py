from typing import List, Optional
from ...schemas.budget import BudgetItem, CreateBudgetItem, DeleteItemData, GetSectionsItemsData
import psycopg2 
from psycopg2.extras import RealDictCursor
import os

class BudgetService:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")

    async def create_budget_item( self, data: CreateBudgetItem ) -> Optional[BudgetItem]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                INSERT INTO budget_items (user_id, section_id, name, amount, type, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING item_id, user_id, section_id, name, amount, type, start_date, end_date
            """

            cur.execute(query, (
                data.user_id,
                data.section_id,
                data.name, 
                data.amount,
                data.type,
                str(data.start_date),
                str(data.end_date) if data.end_date is not None else None
            ))
            response = cur.fetchone()
            conn.commit()

            if response:
                return BudgetItem(**response)
            
            return None
        
        except Exception as e:
            print(f'Error creating item: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()

    async def delete_budget_item( self, data: DeleteItemData ) -> bool:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                DELETE from budget_items
                WHERE user_id = %s AND section_id = %s AND item_id = %s
                RETURNING item_id
            """

            cur.execute(query, (
                data.user_id,
                data.section_id,
                data.item_id
            ))
            response = cur.fetchone()
            conn.commit()

            return bool(response)
        
        except Exception as e:
            print(f'Error deleting item: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()
            
    async def update_budget_item( self, data: BudgetItem ) -> Optional[BudgetItem]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                UPDATE budget_items
                SET 
                    user_id = %s,
                    section_id = %s,
                    name = %s,
                    amount = %s,
                    type = %s,
                    start_date = %s,
                    end_date = %s,
                    updated_at = NOW()
                WHERE item_id = %s
                RETURNING item_id, user_id, section_id, name, amount, type, start_date, end_date
            """

            cur.execute(query, (
                data.user_id,
                data.section_id,
                data.name, 
                data.amount,
                data.type,
                str(data.start_date),
                str(data.end_date) if data.end_date is not None else None,
                data.item_id
            ))
            response = cur.fetchone()
            conn.commit()

            if response:
                return BudgetItem(**response)
            
            return None
        
        except Exception as e:
            print(f'Error creating item: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()

    async def get_sections_items(self, data: GetSectionsItemsData) -> List[BudgetItem]:
            try:
                conn = psycopg2.connect(self.db_url)
                cur = conn.cursor(cursor_factory=RealDictCursor)

                query = """
                    SELECT item_id, user_id, section_id, name, amount, type, start_date, end_date
                    FROM budget_items 
                    WHERE user_id = %s AND section_id = %s
                """

                cur.execute(query, (
                    data.user_id,
                    data.section_id,
                ))
                response = cur.fetchall()

                return [BudgetItem(**item) for item in response]
            
            except Exception as e:
                print(f'Error getting sections items: {str(e)}')
                raise
            finally:
                cur.close()
                conn.close()
            

