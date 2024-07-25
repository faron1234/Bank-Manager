# Category class definition
class Category:
    def __init__(self, name, transactions=None):
        from ..models import TransactionList
        self.name = name
        self.transactions = transactions if transactions else TransactionList()

    def addTransactions(self, transactions):
        self.transactions.transactions.extend(transactions.transactions)
        # Recalculate sums after adding transactions
        self.transactions.getSums()

    def __repr__(self):
        return f"Category(name={self.name}, transactions={self.transactions})"
