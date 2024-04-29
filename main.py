import mysql.connector
import random
import string
import time
from datetime import datetime

conn = mysql.connector.connect(
    user = 'root', 
    database = 'example', 
    password = 'password'
)

cursor = conn.cursor()
def getDate():
    now = datetime.now()
    date = now.strftime("%Y/%m/%d %H:%M:%S CST")
    return date
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

    accountNumber = str(id) + first[0:2].upper() + last[0:2].upper()
    print()
    print("Your account number: " + accountNumber)
    insert_statement = "UPDATE banking SET accountnumber = %s WHERE ID = %s"
    cursor.execute(insert_statement, (accountNumber, id))

    now = datetime.now()
    logs = open("logs.txt", "a")
    logs.write(f"{getDate()} | CREATEACCOUNT | Account {accountNumber} was created (name: {first} {last}, pin: {pin})\n")
    logs.close()

    conn.commit()

def closeAccount():
    accNum = str(input("Enter the account number you want to close: "))
    delete_statement = "DELETE FROM banking WHERE accountnumber = %s"
    val = (accNum,)
    confirm = str(input(f"Are you sure you want to close this ({accNum}) account? "))
    if confirm.lower() == "yes":
        cursor.execute(delete_statement, val)
        print("Account was closed.")

        logs = open("logs.txt", "a")
        logs.write(f"{getDate()} | CLOSEACCOUNT | Account {accNum} was closed\n")
        logs.close()

        conn.commit()
    else:
        print(f"Account ({accNum}) was not closed.")

def modifyAccount():
    while(True):
        print()
        print("Admin Modify Account Screen")
        print("-----------------")
        print("1. Modify Name\n2. Modify PIN\n3. Quit")
        choice = int(input("Choose value: "))

        if choice == 1:
            print()
            accNum = str(input("Enter the account number you want to modify: "))

            select_statement = "SELECT firstname, lastname FROM banking WHERE accountnumber = %s LIMIT 1"
            val = (accNum,)
            cursor.execute(select_statement, val)
            check = cursor.fetchall()
            (oldFirst, oldLast) = check[0]

            newFirst = str(input("Enter new First Name: "))
            newLast = str(input("Enter new Last Name: "))

            val = (newFirst, newLast, accNum)
            update_statement = "UPDATE banking SET firstname = %s, lastname = %s WHERE accountnumber = %s"

            cursor.execute(update_statement, val)
            print("Name was changed in the account " + accNum)
            logs = open("logs.txt", "a")
            logs.write(f"{getDate()} | MODIFYNAME | Account {accNum}'s name was changed {oldFirst} {oldLast} ---> {newFirst} {newLast}\n")
            logs.close()

            conn.commit()
        elif choice == 2:
            print()
            accNum = str(input("Enter the account number you want to modify: "))
            select_statement = "SELECT pin FROM banking WHERE accountnumber = %s LIMIT 1"
            val = (accNum,)
            cursor.execute(select_statement, val)
            check = cursor.fetchall()
            (oldPin) = check[0][0]

            newPin = int(input("Enter new PIN: "))

            val = (newPin, accNum)
            update_statement = "UPDATE banking SET pin = %s WHERE accountnumber = %s"

            cursor.execute(update_statement, val)
            print("PIN was changed in the account " + accNum)

            logs = open("logs.txt", "a")
            logs.write(f"{getDate()} | MODIFYPIN | Account {accNum}'s pin was changed {oldPin} ---> {newPin}\n")
            logs.close()

            conn.commit()
        elif choice == 3:
            break
        else:
            print("Invalid Input\n")

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
        elif choice == 2:
            closeAccount()
        elif choice == 3:
            modifyAccount()
        elif choice == 4:
            break
        else:
            print("Invalid Input\n")
    return False

def checkBalance(accNum, printVal):
    val = (accNum,)
    select_statement = "SELECT balance FROM banking WHERE accountnumber = %s"

    cursor.execute(select_statement, val)
    check = cursor.fetchall()
    (balance) = check[0][0]
    if printVal:
        print()
        print(f"The current balance of account {accNum} is: ${str(balance)}")
        time.sleep(3)
    else:
        return balance
    
def deposit(accNum, ogMoney, printVal):
    oldBalance = checkBalance(accNum, False)
    if printVal:
        print()
        money = float(input("How much money would you like to deposit: "))
    else:
        money = ogMoney
    
    val = (money, accNum)
    update_statement = "UPDATE banking SET balance = balance + %s WHERE accountnumber = %s"
    cursor.execute(update_statement, val)
    newBalance = checkBalance(accNum, False)

    logs = open("logs.txt", "a")
    logs.write(f"{getDate()} | DEPOSIT | ${money} was deposited into account {accNum}, balance changed ${oldBalance} ---> ${newBalance}\n")
    logs.close()

    conn.commit()

    if printVal:
        print(f"${money} has been deposited into account {accNum}")
        checkBalance(accNum, True)
    else:
        return True

def withdraw(accNum, ogMoney, printVal):
    oldBalance = checkBalance(accNum, False)
    if printVal:
        print()
        money = float(input("How much money would you like to withdraw: "))
    else:
        money = ogMoney
    val = (money, accNum)

    if money <= checkBalance(accNum, False):
        if printVal:
            update_statement = "UPDATE banking SET balance = balance - %s WHERE accountnumber = %s"
            cursor.execute(update_statement, val)
            
            print(f"${money} has been withdrawed from account {accNum}")
            checkBalance(accNum, True)
            
            newBalance = checkBalance(accNum, False)
            logs = open("logs.txt", "a")
            logs.write(f"{getDate()} | WITHDRAW | ${money} was withdrawed from account {accNum}, balance changed ${oldBalance} ---> ${newBalance}\n")
            logs.close()

            conn.commit()
        else:
            update_statement = "UPDATE banking SET balance = balance - %s WHERE accountnumber = %s"
            cursor.execute(update_statement, val)

            newBalance = checkBalance(accNum, False)
            logs = open("logs.txt", "a")
            logs.write(f"{getDate()} | WITHDRAW | ${money} was withdrawed from account {accNum}, balance changed ${oldBalance} ---> ${newBalance}\n")
            logs.close()

            conn.commit()
            return True
    else:
        if printVal:
            print("You do not have enough money to make this withdrawal")
            checkBalance(accNum, True)
        else:
            return False
        

def wireTransfer(accNum):
    print()
    transferAcc = str(input("Enter the account number you want to transfer money to: "))
    money = float(input("How much money would you like to transfer: "))

    if withdraw(accNum, money, False):
        if deposit(transferAcc, money, False):
            print(f"${money} was successfully transfered from account {accNum} to account {transferAcc}")

            logs = open("logs.txt", "a")
            logs.write(f"{getDate()} | WIRETRANSFER | ${money} was successfully transfered from account {accNum} to account {transferAcc}\n")
            logs.close()

            checkBalance(accNum, True)
            checkBalance(transferAcc, True)
    else:
        print(f"Account {accNum} does not have enough money to complete the transfer")
        


def userScreen(accNum):
    while(True):
        print()
        print("User Screen")
        print("-----------------")
        print("1. Check Balance\n2. Deposit\n3. Withdraw\n4. Wire Transfer\n5. Log Out")
        choice = int(input("Choose value: "))


        if choice == 1:
            checkBalance(accNum, True)
        elif choice == 2:
            deposit(accNum, None, True)
        elif choice == 3:
            withdraw(accNum, None, True)
        elif choice == 4:
            wireTransfer(accNum)
        elif choice == 5:
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
            accNum = str(input("Enter your account number: ")).upper()
            pin = str(input("Enter your account PIN: "))
            if len(pin) == 4 and pin.isdigit():
                pin = int(pin)
                if login(accNum, pin) == False:
                    print("Could not login, try again.")
                else:
                    if checkAdmin(accNum):
                        if not adminScreen():
                            loggedIn = False
                    else:
                        userScreen(accNum)
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
    print("Thank you for using the bank app!")




if __name__ == '__main__':
    main()