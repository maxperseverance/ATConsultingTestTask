import requests, io
from bs4 import BeautifulSoup
import sqlite3
import logging

URL = r'https://koteekee.ru/receive/papajohns'

conn = sqlite3.connect("pizza.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
with io.open('C:/Users/maks_/Desktop/domodedovo2.html', encoding='utf-8') as html_file:
    soup = BeautifulSoup(html_file, features='html.parser')

pizza = soup.find_all('div', id='pizza')

items = pizza[0].find_all('div', class_='_1iR3FSr_WzuOWyiJFFi4Dc _1OvF7yNvTiif5DFvOSZTuT ProductCard _3UmRR5O-Z31T5VwkD9wpCW')

cards = []
for item in items:
    title = item.find('div', class_='_2SuvxlJZ03zS9Dt2uRiDkq').get_text()
    desc = item.find('div', class_='_1MXqsd4Vrfnk7acAaMe9ve _2uYmw-6znBwRpeYTuDcvPN').get_text()
    type = item.find('div', class_='_22tLg_N-T1_fSuHivc553F gFWUICI_xCcypOmIgwq3L').get_text()
    size = item.find('div', class_='_1zPkLV8_T-7D9zz3ZyyMrt dFaAoXUw74Qmz3XAO1XEV _2WUWliRAOSTDfCeSHCQbW _1qY9g378gz7kNHM4beS3i').get_text().split()[0]
    price = item.find('div', class_='AkOaPdzKXXkN8Vsguj3lh _3ZxcheiXBqcNXPHFDFBcmo').get_text().split()[0]

    cardDict = {
        'title': title,
        'desc':desc,
        'type': type,
        'size': size,
        'price': price
    }

    print('Parsed item', cardDict)
    response = requests.post(URL, cardDict).json()
    print('Got response', response)

    id = response['response_uuid']
    cardDict['id'] = id
    cards.append([id, title, desc, type, size, price])

print(cards)
cursor.executemany("INSERT INTO pizzas VALUES (?,?,?,?,?,?)", cards)
conn.commit()