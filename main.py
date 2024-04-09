import mysql.connector
import random
import time

conn = mysql.connector.connect(user = 'root', database = 'example', password = 'password')

cursor = conn.cursor()

testQuery = ("SELECT * FROM banking")
cursor.execute(testQuery)

for item in cursor:
    print(item)

def addUsers(conn, cursor, name, age, grade, gpa):
    insert_statement = ("INSERT INTO student (name, age, grade, gpa) VALUES (?, ?, ?, ?)")
    cursor.execute(insert_statement, (name, age, grade, gpa))
    conn.commit()

cursor.close()
conn.close()

def main():
    print("Welcome to the bank app.")
    pin1 = random.randint(0, 9)
    pin2 = random.randint(0, 9)
    pin3 = random.randint(0, 9)
    pin4 = random.randint(0, 9)
    correctPIN = str(pin1 + pin2 + pin3 + pin4)
    accountID = str(input("Enter your account number: "))
    accountPIN = str(input("Enter your account PIN: "))
    count = 0
    while(accountPIN != correctPIN and count < 3):
        accountPIN = str(input("Incorrect PIN. Please enter again: "))
