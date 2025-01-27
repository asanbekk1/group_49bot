import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS dishes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                description TEXT,
                                category TEXT NOT NULL,
                                portion_sizes TEXT,
                                image_url TEXT
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

    def save_dish(self, name, price, description, category, portion_sizes, image_url=None):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''INSERT INTO dishes (name, price, description, category, portion_sizes, image_url)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                         (name, price, description, category, portion_sizes, image_url))

    def get_dishes(self, sort_by='name', order='ASC', limit=10, offset=0):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute(f'''SELECT * FROM dishes ORDER BY {sort_by} {order} LIMIT {limit} OFFSET {offset}''')
            return cursor.fetchall()

    def get_dish_by_id(self, dish_id):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute('''SELECT * FROM dishes WHERE id = ?''', (dish_id,))
            return cursor.fetchone()

    def update_dish(self, dish_id, name=None, price=None, description=None, category=None, portion_sizes=None,
                    image_url=None):
        with sqlite3.connect(self.path) as conn:
            query = "UPDATE dishes SET "
            params = []
            if name:
                query += "name = ?, "
                params.append(name)
            if price:
                query += "price = ?, "
                params.append(price)
            if description:
                query += "description = ?, "
                params.append(description)
            if category:
                query += "category = ?, "
                params.append(category)
            if portion_sizes:
                query += "portion_sizes = ?, "
                params.append(portion_sizes)
            if image_url:
                query += "image_url = ?, "
                params.append(image_url)

            query = query.rstrip(', ')  # Убираем последнюю запятую
            query += " WHERE id = ?"
            params.append(dish_id)
            conn.execute(query, tuple(params))

    def delete_dish(self, dish_id):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''DELETE FROM dishes WHERE id = ?''', (dish_id,))

    def save_review(self, user_id, name, instagram_username, rating, extra_comments, visit_date):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''INSERT INTO reviews (user_id, name, instagram_username, rating, extra_comments, visit_date)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                         (user_id, name, instagram_username, rating, extra_comments, visit_date))

    def get_recent_reviews(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute('''SELECT * FROM reviews WHERE visit_date >= date('now', '-3 days')''')
            return cursor.fetchall()
