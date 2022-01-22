import sqlite3


def send_user(sender, receiver, amount):
    con = sqlite3.connect("db/tips.db")
    cur = con.cursor()
    daten = cur.execute("SELECT * FROM data")
    senderGefunden = False
    receiverGefunden = False
    for i in daten:
        print(i)
        if i[0] == sender:
            senderGefunden = True
            balanceSender = str(i[1])
        elif i[0] == receiver:
            receiverGefunden = True
            balanceReceiver = str(i[1])

    if senderGefunden == True & receiverGefunden == True:
        if int(balanceSender) >= amount:
            wertNeuSender = int(balanceSender) - amount
            wertNeuReceiver = int(balanceReceiver) + amount
            cur.execute("UPDATE data SET balance = " + str(wertNeuSender) + " WHERE user=\'" + sender + "\'")
            cur.execute("UPDATE data SET balance = " + str(wertNeuReceiver) + " WHERE user=\'" + receiver + "\'")
            con.commit()
                    
            print("Zahlung erfolgreich")
            return 0
        else:
            print("Nicht genügend Geld")
            return 1
    elif senderGefunden == False:
        cur.execute("INSERT INTO data VALUES (\'" + str(sender) + "\',0)")
        con.commit()
        con.close()
        send_user(sender,receiver,amount)
    elif receiverGefunden == False:
        cur.execute("INSERT INTO data VALUES (\'" + str(receiver) + "\',0)")
        con.commit()
        con.close()
        send_user(sender,receiver,amount)
    con.close()

def get_balance(user):
    con = sqlite3.connect("db/tips.db")
    cur = con.cursor()
    daten = cur.execute("SELECT * FROM data")
    for i in daten:
        if i[0] == user:
            print(i[1])
            return i[1]

def deposit(user, amount):
    con = sqlite3.connect("db/tips.db")
    cur = con.cursor()
    daten = cur.execute("SELECT * FROM data")
    for i in daten:
        if i[0] == user:
            balance = i[1]
            balanceNeu = int(i[1]) + int(amount)
            cur.execute("UPDATE data SET balance = " + str(balanceNeu) + " WHERE user=\'" + user + "\'")
            
        else:
            cur.execute("INSERT INTO data VALUES (\'" + str(user) + "\'," + str(amount) + ")")
    con.commit()
    con.close()    