from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from typing import Optional

class DatabaseManager:
    """
    """
    def __init__(self):
        """
        """
        self.pool: Optional[ConnectionPool] = None

    def initialize(self, Connection_string: str):
        """

        """
        if not Connection_string:
            print("No database connection string provided")
            return
            
        self.pool = ConnectionPool(
            conninfo=Connection_string,
            min_size=20,
            kwargs={"autocommit": True, "prepare_threshold": 0}
            )

        #setuo the checkpoint saver
        with self.pool.connection() as conn:
            saver = PostgresSaver(conn)
            saver.setup()

    def close(self):
        """
        """
        if self.pool:
            self.pool.close()

    def get_saver(self) -> Optional[PostgresSaver]:
        """
        """
        if not self.pool:
            return None

        return PostgresSaver(self.pool)

db_manager = DatabaseManager()