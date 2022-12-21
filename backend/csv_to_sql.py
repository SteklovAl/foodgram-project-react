import csv

import psycopg2

connection = psycopg2.connect(host='db',
                              dbname='postgres',
                              user='postgres',
                              password='postgres',
                              port='5432')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE if not exists recipes_ingredient(
    name varchar,
    measurement_unit varchar
)
''')

with open('D:/Dev/foodgram-project-react/backend/ingredients.csv',
          'r', encoding='utf8') as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(
        i['name'], i['measurement_unit'])
        for i in dr
    ]
cursor.executemany('INSERT INTO recipes_ingredient (name, measurement_unit) '
                   'VALUES (%s, %s);', to_db)

connection.commit()
connection.close()
