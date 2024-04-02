import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'example', password = 'password')

cursor = connection.cursor()

testQuery = ("SELECT * FROM banking")
cursor.execute(testQuery)

for item in cursor:
    print(item)

cursor.close()
connection.close()