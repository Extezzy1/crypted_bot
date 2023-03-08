import sqlite3


class Database:

    def __init__(self, file_db):
        self.connection = sqlite3.connect(file_db)
        self.cursor = self.connection.cursor()

    def exist_user(self, user_id):
        with self.connection:
            return bool(len(self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, )).fetchmany(1)))

    def add_user(self, user_id, first_last, username):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)", (user_id, first_last, username))
