import psycopg2

connection = psycopg2.connect(host='localhost',
                              dbname='postgres',
                              user='postgres',
                              password='postgres',
                              port='5432')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE if not exists ingredient(
    name varchar,
    measurement_unit varchar
)
""")

with open('D:/Dev/foodgram-project-react/data/ingredients.json') as file:
    data = file.read()

query_sql = """
insert into ingredient select * from
json_populate_recordset(NULL::ingredient, %s);
"""

cursor.execute(query_sql, (data,))
connection.commit()
