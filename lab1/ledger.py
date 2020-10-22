import sqlite3
import datetime

db = sqlite3.connect("ledger.db")
cursor = db.cursor()
cursor.execute("PRAGMA foreign_keys = ON")
trans_id = 0


def prep():
    cursor.execute('''DROP TABLE IF EXISTS accounts''')
    cursor.execute('''DROP TABLE IF EXISTS transactions''')


def init_db():
    cursor.execute('''CREATE table accounts (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        bankName TEXT,
        credit INTEGER)''')
    cursor.execute('''CREATE table transactions (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account INTEGER,
            to_account INTEGER,
            fee INTEGER,
            amount INTEGER,
            transactionDateTime TEXT,
            FOREIGN KEY (from_account) REFERENCES accounts(_id),
            FOREIGN KEY (to_account) REFERENCES accounts(_id))''')


def fill_db():
    accounts = [(1, 'Account 1', 'SpearBank', 1000), (2, 'Account 2', 'Tinkoff', 1000),
                (3, 'Account 3', 'SpearBank', 1000), (4, 'Account 4', 'Fee', 0)]
    cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?)", accounts)


def print_accounts():
    cursor.execute("SELECT * FROM accounts")
    print("Accounts info:")
    for acc in cursor.fetchall():
        print("Credit for {} with id: {} is {} RUB".format(acc[1], acc[0], acc[3]))
    print()


def print_transactions():
    cursor.execute("SELECT * FROM transactions")
    print("Transaction info:")
    for trans in cursor.fetchall():
        print("Transaction with id: {} was performed on: {}. {} RUB were transferred from {} to {} with fee {} RUB."\
            .format(trans[0], trans[5], trans[4], trans[1], trans[2], trans[3]))
    print()


def pay_fee(acc1, credit1, fee):
    if fee == 0:
        return
    cursor.execute("SELECT credit FROM accounts WHERE name='Account 4'")
    fee_credit = cursor.fetchall()[0][0]
    cursor.execute('''UPDATE accounts
            SET credit = ?1
            WHERE name = ?2''', (fee_credit + fee, 'Account 4'))


def register(from_acc, to_acc, fee, amount):
    global trans_id
    cursor.execute("SELECT _id FROM accounts WHERE name=?", [from_acc])
    id1 = cursor.fetchall()[0][0]
    cursor.execute("SELECT _id FROM accounts WHERE name=?", [to_acc])
    id2 = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)",
                   (trans_id, id1, id2, fee, amount, datetime.datetime.now().__str__()))
    trans_id += 1


def transfer(acc1, acc2, amount):
    fee = 0
    cursor.execute("SELECT credit, bankName FROM accounts WHERE name=?", [acc1])
    res = cursor.fetchall()[0]
    credit1 = res[0]
    bank1 = res[1]
    cursor.execute("SELECT credit, bankName FROM accounts WHERE name=?", [acc2])
    res = cursor.fetchall()[0]
    credit2 = res[0]
    bank2 = res[1]
    if bank1 != bank2:
        fee = 30
    if credit1 < (amount + fee):
        print("Sender don't have enough credit to perform the transaction. Transaction was not completed")
        return
    pay_fee(acc1, credit1, fee)
    cursor.execute('''UPDATE accounts
        SET credit = ?1
        WHERE name = ?2''', (credit1 - amount - fee, acc1))
    cursor.execute('''UPDATE accounts
        SET credit = ?1
        WHERE name = ?2''', (credit2 + amount, acc2))
    register(acc1, acc2, fee, amount)
