import sqlite3

db = sqlite3.connect("ledger.db")
cursor = db.cursor()
cursor.execute("PRAGMA foreign_keys = ON")


def prep():
    cursor.execute('''DROP TABLE IF EXISTS accounts''')


def init_db():
    cursor.execute('''CREATE table accounts (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        credit INTEGER)''')


def fill_db():
    accounts = [(1, 'Account 1', 1000), (2, 'Account 2', 1000), (3, 'Account 3', 1000)]
    cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?)", accounts)


def print_accounts():
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    for acc in accounts:
        print("Credit for {} is {} RUB".format(acc[1], acc[2]))


def transfer(acc1, acc2, amount):
    cursor.execute("SELECT credit FROM accounts WHERE name=?", [acc1])
    credit1 = cursor.fetchall()[0][0]
    cursor.execute("SELECT credit FROM accounts WHERE name=?", [acc2])
    credit2 = cursor.fetchall()[0][0]
    if credit1 < amount:
        print("Sender don't have enough credit to perform the transaction. Transaction was not completed")
        return
    cursor.execute('''UPDATE accounts
        SET credit = ?1
        WHERE name = ?2''', (credit1 - amount, acc1))
    cursor.execute('''UPDATE accounts
        SET credit = ?1
        WHERE name = ?2''', (credit2 + amount, acc2))
