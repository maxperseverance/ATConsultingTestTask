import requests, io
from bs4 import BeautifulSoup
import sqlite3

URL = r'https://koteekee.ru/receive/papajohns'
DB_NAME = "pizza.db"
TABLE_NAME = "pizzas"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS " + TABLE_NAME)

cursor.execute("""CREATE TABLE """ + TABLE_NAME + """
                  (id text PRIMARY KEY, title text, desc text, type text,
                   price float, size float)
               """)

with io.open('C:/Users/maks_/Desktop/domodedovo2.html', encoding='utf-8') as html_file:
    soup = BeautifulSoup(html_file, features='html.parser')

pizza = soup.find_all('div', id='pizza')

items = pizza[0].find_all('div',
                          class_='_1iR3FSr_WzuOWyiJFFi4Dc _1OvF7yNvTiif5DFvOSZTuT ProductCard _3UmRR5O-Z31T5VwkD9wpCW')

cards = []
for item in items:
    title = item.find('div', class_='_2SuvxlJZ03zS9Dt2uRiDkq').get_text()
    desc = item.find('div', class_='_1MXqsd4Vrfnk7acAaMe9ve _2uYmw-6znBwRpeYTuDcvPN').get_text()
    type = item.find('div', class_='_22tLg_N-T1_fSuHivc553F gFWUICI_xCcypOmIgwq3L').get_text()
    size = item.find('div',
                     class_='_1zPkLV8_T-7D9zz3ZyyMrt dFaAoXUw74Qmz3XAO1XEV _2WUWliRAOSTDfCeSHCQbW _1qY9g378gz7kNHM4beS3i').get_text().split()[
        0]
    price = item.find('div', class_='AkOaPdzKXXkN8Vsguj3lh _3ZxcheiXBqcNXPHFDFBcmo').get_text().split()[0]

    cardDict = {
        'title': title,
        'desc': desc,
        'type': type,
        'size': size,
        'price': price
    }

    print('Parsed item', cardDict)
    response = requests.post(URL, cardDict)
    if response.status_code != 200:
        print("Got bad response with code", response.status_code)
        exit(0)

    response = response.json()
    print('Got response', response)

    id = response['response_uuid']
    cards.append([id, title, desc, type, size, price])

cursor.executemany("INSERT INTO " + TABLE_NAME + " VALUES (?,?,?,?,?,?)", cards)  # prevent sql injection
conn.commit()
