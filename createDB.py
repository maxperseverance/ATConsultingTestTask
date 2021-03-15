import sqlite3

conn = sqlite3.connect("pizza.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE pizzas
                  (id text PRIMARY KEY, title text, desc text, type text,
                   price float, size float)
               """)