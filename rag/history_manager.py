import sqlite3
from datetime import datetime


class HistoryManager:
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """初始化数据库，创建聊天记录表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # role：区分用户和Bot，
        # sender_name：存储具体是谁说的，
        # nteract_with: 这场对话的归属人，
        # content：消息内容，
        # timestamp：消息时间
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role TEXT NOT NULL,
                        sender_name TEXT NOT NULL,
                        interact_with TEXT NOT NULL, 
                        content TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
        conn.commit()
        conn.close()

    def add_message(self, role: str, sender_name: str, interact_with: str, content: str):
        """保存一条新消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            'INSERT INTO messages (role, sender_name, interact_with, content, timestamp) VALUES (?, ?, ?, ?, ?)',
            (role, sender_name, interact_with, content, now_str)
        )
        conn.commit()
        conn.close()

    def get_recent_history(self, target_user, limit: int = 5) -> str:
        """获取用户与模型最近limit条对话历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # 按照时间倒序查出最近的 limit 条
        cursor.execute('''
                    SELECT role, sender_name, content 
                    FROM messages 
                    WHERE interact_with = ?
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (target_user, limit))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "暂无近期聊天记录。"

        # rows.reverse()

        history_str = ""
        for role, sender, content in rows:
            # 拼装成提示词需要的格式
            history_str += f"{sender}: {content}\n"

        return history_str.strip()


if __name__ == "__main__":
    db = HistoryManager("test_history.db")

    db.add_message(role="user", sender_name="zd", interact_with="zd", content="来财吗？")
    db.add_message(role="bot", sender_name="米粒", interact_with="zd", content="来个屁，真谢了。")

    db.add_message(role="user", sender_name="lyc", interact_with="lyc", content="今天天气好热")
    db.add_message(role="bot", sender_name="米粒", interact_with="lyc", content="你自己开窗户看啊。")

    db.add_message(role="user", sender_name="zd", interact_with="zd", content="你什么态度？")


    print(db.get_recent_history(target_user="zd", limit=5))