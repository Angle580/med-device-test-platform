import pymysql
import logging

logger = logging.getLogger(__name__)

class DBUtil:
    """MySQL 连接 + 测试断言工具"""

    def __init__(self, host, user, password, db, port=3306):
        self.conn = pymysql.connect(
            host=host, port=port, user=user, password=password,
            database=db, cursorclass=pymysql.cursors.DictCursor,
            charset="utf8mb4",
        )

    def query_one(self, sql: str) -> dict:
        with self.conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchone()

    def query_all(self, sql: str) -> list:
        with self.conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def execute(self, sql: str):
        with self.conn.cursor() as cur:
            cur.execute(sql)
        self.conn.commit()

    def assert_db_equal(self, table: str, record_id: int, field: str, expected):
        row = self.query_one(f"SELECT {field} FROM {table} WHERE id={record_id}")
        actual = row[field] if row else None
        assert actual == expected, \
            f"DB校验失败: 表={table} id={record_id} 字段={field} 期望={expected} 实际={actual}"

    def count_rows(self, table: str, where: str = "") -> int:
        sql = f"SELECT COUNT(*) AS c FROM {table}"
        if where:
            sql += f" WHERE {where}"
        row = self.query_one(sql)
        return row["c"]

    def close(self):
        self.conn.close()
