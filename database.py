import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            portion_sizes TEXT
        )
        ''')
        self.connection.commit()

    def add_dish(self, name, price, description, category, portion_sizes):
        """Метод для добавления нового блюда в таблицу"""
        # Сохранение данных в таблицу dishes
        self.cursor.execute('''
        INSERT INTO dishes (name, price, description, category, portion_sizes)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, price, description, category, portion_sizes))
        self.connection.commit()
        print(f"Блюдо '{name}' добавлено в меню!")

    def close(self):
        self.connection.close()


def admin_interface():
    print("Добро пожаловать в панель администратора!")
    name = input("Введите название блюда: ")
    price = float(input("Введите цену блюда: "))
    description = input("Введите описание блюда: ")
    print("Категории блюд: первое, второе, пицца, горячие напитки, холодные напитки, салаты, горячительные напитки")
    category = input("Введите категорию блюда: ")
    portion_sizes = input("Введите варианты порций (через запятую): ")

    db = Database("restaurant_menu.db")
    db.add_dish(name, price, description, category, portion_sizes)
    db.close()


if __name__ == "__main__":
    db = Database("restaurant_menu.db")
    db.create_tables()
    db.close()

    admin_interface()
