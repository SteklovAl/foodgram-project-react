import csv

import psycopg2

connection = psycopg2.connect(host='127.0.0.1',
                              dbname='postgres',
                              user='postgres',
                              password='postgres',
                              port='5432')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE if not exists recipes_ingredient(
    name varchar,
    measurement_unit varchar
)
""")

with open('D:/Dev/foodgram-project-react/data/ingredients.csv', 'r', encoding="utf8") as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(
        i['name'], i['measurement_unit'])
        for i in dr
    ]
cursor.executemany("INSERT INTO recipes_ingredient (name, measurement_unit) "
                   "VALUES (%s, %s);", to_db)

connection.commit()
connection.close()

# import sqlite3

# conn = sqlite3.connect('C:/Dev/api_yamdb/api_yamdb/db.sqlite3')
# cursor = conn.cursor()

# cursor.execute("""select * from sqlite_master
#             where type = 'table'""")
# tables = cursor.fetchall()

# for table in tables:
#     print(table)  # информация о таблицах
#     print(table[1]) # названия тадлиц
