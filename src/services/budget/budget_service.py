from typing import List, Optional

from src.schemas.transactions import Transaction
from ...schemas.budget import BudgetItem, BudgetItems, CreateBudgetItem, DeleteItemData, GetBudgetData
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
                INSERT INTO budget_items (user_id, section_name, name, amount, type, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING item_id, user_id, section_name AS section, name, amount, type, start_date, end_date
            """

            cur.execute(query, (
                data.user_id,
                data.section,
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
                WHERE user_id = %s AND section_name = %s AND item_id = %s
                RETURNING item_id
            """

            cur.execute(query, (
                data.user_id,
                data.section,
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
                    section_name = %s,
                    name = %s,
                    amount = %s,
                    type = %s,
                    start_date = %s,
                    end_date = %s,
                    updated_at = NOW()
                WHERE item_id = %s
                RETURNING item_id, user_id, section_name AS section, name, amount, type, start_date, end_date
            """

            cur.execute(query, (
                data.user_id,
                data.section,
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

    async def get_budget(self, data: GetBudgetData) -> List[BudgetItems]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            # Fetch budget items
            budget_query = """
                SELECT item_id, user_id, section_name AS section, name, amount, type, start_date, end_date
                FROM budget_items 
                WHERE 
                    user_id = %s 
                    AND EXTRACT(YEAR FROM start_date) = %s
                    AND EXTRACT(MONTH FROM start_date) <= %s
                    AND (
                        end_date IS NULL 
                        OR (
                            EXTRACT(YEAR FROM end_date) = %s
                            AND EXTRACT(MONTH FROM end_date) >= %s
                        )
                    );
            """
            cur.execute(budget_query, (
                data.user_id, data.year, data.month, data.year, data.month
            ))
            budget_items = cur.fetchall()

            # Fetch transactions
            transactions_query = """
                SELECT transaction_id, user_id, item_id, description, amount, type, date
                FROM item_transactions 
                WHERE 
                    user_id = %s
                    AND EXTRACT(MONTH FROM date) = %s
                    AND EXTRACT(YEAR FROM date) = %s
            """
            cur.execute(transactions_query, (data.user_id, data.month, data.year))
            transactions = cur.fetchall()

            # Organize transactions by item_id
            transactions_by_item = {}
            for transaction in transactions:
                item_id = transaction["item_id"]
                if item_id not in transactions_by_item:
                    transactions_by_item[item_id] = []
                transactions_by_item[item_id].append(Transaction(**transaction))

            print(f"Transactions by item: {transactions_by_item}")

            # Assign transactions to budget items
            budget_items_list = []
            for item in budget_items:
                item_id = item["item_id"]
                item["transactions"] = transactions_by_item.get(item_id, [])
                budget_items_list.append(BudgetItems(**item))

            return budget_items_list
        
        except Exception as e:
            print(f'Error getting sections items: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()
            

