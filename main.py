import mysql.connector
import random
import string

conn = mysql.connector.connect(
    user = 'root', 
    database = 'example', 
    password = 'password'
)

cursor = conn.cursor()

def checkTable():
    testQuery = ("SELECT * FROM banking")
    cursor.execute(testQuery)

    for item in cursor:
        print(item)

def checkAdmin(accNum):
    sql = "SELECT admin FROM banking WHERE accountnumber = %s"
    val = (accNum,)
    cursor.execute(sql, val)

    check = cursor.fetchall()
    (adminPerm) = check[0][0]

    if adminPerm == 1:
        return True
    return False


def createAccount():
    first = str(input("Enter your First Name: "))
    last = str(input("Enter your Last Name: "))
    pin = int(input("Enter an account PIN: "))

    create_statement = "INSERT INTO banking (firstname, lastname, pin) VALUES (%s, %s, %s)"
    val = (first, last, pin)
    cursor.execute(create_statement, val)

    select_statement = "SELECT LAST_INSERT_ID()"
    cursor.execute(select_statement)
    check = cursor.fetchall()
    (id) = check[0][0]
    print(id)

    accountNumber = str(id) + first[0:2].upper() + last[0:2].upper()
    print(accountNumber)
    insert_statement = "UPDATE banking SET accountnumber = %s WHERE ID = %s"
    cursor.execute(insert_statement, (accountNumber, id))

    conn.commit()

def login(accNum, pin):
    sql = "SELECT accountnumber, pin FROM banking WHERE accountnumber = %s AND pin = %s LIMIT 1"
    val = (accNum, pin)
    cursor.execute(sql, val)
    check = cursor.fetchall()
    if not check:
        return False
    else:
        (sqlNum, sqlPIN) = check[0]

        if sqlNum == id and sqlPIN == pin:
            return True

def adminScreen():
    while(True):
        print()
        print("Admin Screen")
        print("-----------------")
        print("1. Create Account\n2. Close Account\n3. Modify Account\n4. Log Out")
        choice = int(input("Choose value: "))


        if choice == 1:
            createAccount()
        #elif choice == 2:
            #closeAccount()
        #elif choice == 3:
            #modifyAccount()
        elif choice == 4:
            break
        else:
            print("Invalid Input\n")
    return False


    

#createAccount(conn, cursor, 3, 'Steve Jobs', 1234, 152.54)
checkTable()

def main():
    print("Welcome to the bank app.")
    loggedIn = True
    quitApp = True
    while(quitApp):
        while(loggedIn):
            print()
            accNum = str(input("Enter your account number: "))
            pin = str(input("Enter your account PIN: "))
            if len(pin) == 4 and pin.isdigit():
                pin = int(pin)
                if login(accNum, pin) == False:
                    print("Could not login, try again.")
                else:
                    if checkAdmin(accNum):
                        if not adminScreen():
                            loggedIn = False
        while(True):
            print()
            quit = str(input("Would you like to quit the app? (yes/no): "))
            if quit == "yes":
                quitApp = False
                break
            elif quit == "no":
                loggedIn = True
                break
            else:
                print("Invalid Input")




if __name__ == '__main__':
    main()