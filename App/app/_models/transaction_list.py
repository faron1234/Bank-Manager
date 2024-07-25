from ...static import Sorts


# TransactionList class definition
class TransactionList:
    def __init__(self, transactions=None):
        self.totalTransactions = 0
        self.transactions = transactions if transactions is not None else []
        self.outSum = 0.0
        self.inSum = 0.0
        self.change = 0.0
        self.getSums() if transactions else None

    # Calculate sums of transactions
    def getSums(self):
        self.outSum = 0.0
        self.inSum = 0.0
        for transaction in self.transactions:
            if transaction.amount > 0:
                self.inSum += transaction.amount
            else:
                self.outSum += abs(transaction.amount)
        self.change = self.inSum - self.outSum

    # Add transaction to the list
    def add(self, transaction):
        if not any(existing.desc == transaction.desc and existing.date == transaction.date and existing.amount == transaction.amount and existing.balBefore == transaction.balBefore and existing.balAfter == transaction.balAfter for existing in self.transactions):
            self.transactions.append(transaction)
            self.totalTransactions += 1
            # static.logging.error(f"Added transaction: {transaction}")

    # Remove transaction from the list
    def remove(self, transaction):
        if transaction in self.transactions:
            self.transactions.remove(transaction)
            self.totalTransactions -= 1
            # static.logging.info(f"Removed transaction: {transaction}")
        else:
            # static.logging.warning(f"Attempted to remove non-existent transaction: {transaction}")
            pass

    # Get subset of transactions based on keywords
    def getSubset(self, keywords=None, start_date=None, end_date=None):
        subset = self.transactions

        if keywords:
            subset = [transaction for transaction in subset if
                      any(keyword.lower() in transaction.desc.lower() for keyword in keywords)]
        if start_date:
            subset = [transaction for transaction in subset if transaction.date >= start_date]

        if end_date:
            subset = [transaction for transaction in subset if transaction.date <= end_date]

        return subset

    # Sort transactions based on sort value
    def sort(self, sortValue, sortDirection='asc'):
        if sortValue == Sorts.dateSort:
            self.transactions.sort(key=lambda transaction: transaction.date, reverse=(sortDirection == 'desc'))
        elif sortValue == Sorts.descSort:
            self.transactions.sort(key=lambda transaction: transaction.desc.lower(),
                                   reverse=(sortDirection == 'desc'))
        elif sortValue == Sorts.amountSort:
            self.transactions.sort(key=lambda transaction: abs(transaction.amount),
                                   reverse=(sortDirection == 'desc'))
        # static.logging.info(f"Sorted transactions by {sortValue} in {'descending' if sortDirection == 'desc' else 'ascending'} order: {self.transactions}")

    def amount(self):
        return self.totalTransactions

    def __repr__(self):
        return f"TransactionList(totalTransactions={self.totalTransactions}, transactions={self.transactions})"
