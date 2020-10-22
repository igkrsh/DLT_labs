import ledger


def exercise1():
    ledger.prep()
    ledger.init_db()
    ledger.fill_db()
    ledger.print_accounts()
    ledger.transfer('Account 1', 'Account 3', 500)
    ledger.transfer('Account 2', 'Account 1', 700)
    ledger.transfer('Account 2', 'Account 3', 100)
    ledger.print_accounts()
    ledger.print_transactions()


exercise1()
