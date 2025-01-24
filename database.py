import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS dishes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                description TEXT,
                                category TEXT NOT NULL,
                                portion_sizes TEXT
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                name TEXT,
                                instagram_username TEXT,
                                rating INTEGER,
                                extra_comments TEXT,
                                visit_date TEXT
                            )''')

    def save_dish(self, name, price, description, category, portion_sizes):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''INSERT INTO dishes (name, price, description, category, portion_sizes)
                            VALUES (?, ?, ?, ?, ?)''', (name, price, description, category, portion_sizes))

    def get_dishes(self, sort_by='name', order='ASC'):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute(f'''SELECT * FROM dishes ORDER BY {sort_by} {order}''')
            return cursor.fetchall()

    def get_recent_reviews(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute('''SELECT * FROM reviews WHERE visit_date >= date('now', '-3 days')''')
            return cursor.fetchall()


