
import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
                                CREATE TABLE IF NOT EXISTS reviews (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    name TEXT,
                                    instagram_username TEXT,
                                    rating INTEGER,
                                    extra_comments TEXT,
                                    visit_date TEXT
                                )''')
            conn.execute('''
                            CREATE TABLE IF NOT EXISTS dishes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                description TEXT,
                                category TEXT NOT NULL,
                                portion_sizes TEXT
                            )
                            ''')

    def save_review(self, data, visit_date):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
                        INSERT INTO reviews (name, instagram_username, rating, extra_comments, visit_date)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (
            data['name'], data['instagram_username'], data['rating'], data['extra_comments'], visit_date,))


    def save_dish(self, name, price, description, category, portion_sizes):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
                    INSERT INTO dishes (name, price, description, category, portion_sizes)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (name, price, description, category, portion_sizes))


