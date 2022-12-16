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

with open('D:/Dev/foodgram-project-react/data/ingredients.json') as file:
    data = file.read()

query_sql = """
insert into recipes_ingredient select * from
json_populate_recordset(id::recipes_ingredient, %s);
"""

cursor.execute(query_sql, (data,))
connection.commit()
