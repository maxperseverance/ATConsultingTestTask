import sqlite3

conn = sqlite3.connect("pizza.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""CREATE TABLE pizzas
                  (id text PRIMARY KEY, title text, desc text, type text,
                   price float, size float)
               """)