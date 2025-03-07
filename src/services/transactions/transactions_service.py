from typing import List, Optional
from ...schemas.transactions import Transaction, CreateTransactionData, DeleteTransactionData, GetAllTransactionsData, GetMonthsTransactionsData
import psycopg2  # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
import os

class TransactionService:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
    
    async def create_transaction( self, data: CreateTransactionData ) -> Optional[Transaction]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                INSERT INTO item_transactions (user_id, item_id, description, amount, type, date)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING transaction_id
            """

            cur.execute(query, (
                data.user_id,
                data.item_id,
                data.description,
                data.amount,
                data.type,
                str(data.date)
            ))
            response = cur.fetchone()
            conn.commit()

            if response:
                return Transaction (
                    transaction_id=response["transaction_id"],
                    user_id=data.user_id,
                    item_id=data.item_id,
                    description=data.description,
                    amount=data.amount,
                    type=data.type,
                    date=data.date
                )
            
            return None
        
        except Exception as e:
            print(f'Error creating transaction: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()

    async def update_transaction( self, data: DeleteTransactionData ) -> bool:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                UPDATE item_transactions 
                SET
                    user_id = %s, 
                    item_id = %s, 
                    description = %s, 
                    amount = %s, 
                    type = %s, 
                    date = %s
                WHERE transaction_id = %s
                RETURNING transaction_id, user_id, item_id, description, amount, type, date
            """

            cur.execute(query, (
                data.user_id,
                data.item_id,
                data.description,
                data.amount,
                data.type,
                str(data.date),
                data.transaction_id
            ))
            response = cur.fetchone()
            conn.commit()

            if response:
                return Transaction(**response)
            
            return None
        
        except Exception as e:
            print(f'Error updating transaction: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()

    async def delete_transaction( self, data: Transaction ) -> Optional[Transaction]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                DELETE from item_transactions 
                WHERE user_id = %s AND transaction_id = %s
                RETURNING transaction_id
            """

            cur.execute(query, (
                data.user_id,
                data.transaction_id
            ))
            response = cur.fetchone()
            conn.commit()

            if response:
                return True
            return False
        
        except Exception as e:
            print(f'Error deleting transaction: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()

    async def get_all_transactions( self, data: GetAllTransactionsData ) -> List[Transaction]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                SELECT transaction_id, user_id, item_id, description, amount, type, date
                FROM item_transactions 
                WHERE user_id = %s
            """

            cur.execute(query, (data.user_id,))
            transactions = cur.fetchall()

            if transactions:
                return [Transaction(**transaction) for transaction in transactions]
            
            return []
        
        except Exception as e:
            print(f'Error getting transactions: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()

    async def get_months_transactions( self, data: GetMonthsTransactionsData ) -> List[Transaction]:
        try:
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

            query = """
                SELECT transaction_id, user_id, item_id, description, amount, type, date
                FROM item_transactions 
                WHERE 
                    user_id = %s
                    AND EXTRACT(MONTH FROM date) = %s
                    AND EXTRACT(YEAR FROM date) = %s
            """

            cur.execute(query, (
                data.user_id,
                data.month, 
                data.year,
            ))
            transactions = cur.fetchall()

            if transactions:
                return [Transaction(**transaction) for transaction in transactions]
            
            return []
        
        except Exception as e:
            print(f'Error getting transactions: {str(e)}')
            raise
        finally:
            cur.close()
            conn.close()