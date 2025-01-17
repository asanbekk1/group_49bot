import sqlite3


class Database:
def init_db():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        instagram_username TEXT,
        rating INTEGER,
        extra_comments TEXT,
        visit_date TEXT
    )''')


def save_review(data, visit_date):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO reviews (name, instagram_username, rating, extra_comments, visit_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['instagram_username'], data['rating'], data['extra_comments'], visit_date))


