import csv
from datetime import datetime
from ..static import Sorts


def parseCurrency(value):
    try:
        value = value.replace('£', '').replace(',', '').strip()
        return float(value) if value else 0.0
    except ValueError:
        # static.logging.error(f"Error parsing currency value: '{value}'")
        return 0.0


# Transaction class definition
class Transaction:
    def __init__(self, date, transactionType, description, paidOut, paidIn, balance):
        self.date = datetime.strptime(date, "%d %b %Y")  # Assuming date is in "dd/mm/yyyy" format
        self.type = transactionType
        self.desc = description
        self.amount = parseCurrency(paidIn) - parseCurrency(paidOut)
        self.balAfter = parseCurrency(balance)
        self.balBefore = self.balAfter - self.amount

    def __repr__(self):
        return f"Transaction(date={self.date}, type={self.type}, desc={self.desc}, amount={self.amount}, balAfter={self.balAfter})"


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


# Category class definition
class Category:
    def __init__(self, name, transactions=None):
        self.name = name
        self.transactions = transactions if transactions else TransactionList()

    def addTransactions(self, transactions):
        self.transactions.transactions.extend(transactions.transactions)
        # Recalculate sums after adding transactions
        self.transactions.getSums()

    def __repr__(self):
        return f"Category(name={self.name}, transactions={self.transactions})"


# Account class definition
class Account:
    def __init__(self, name, bank):
        self.name = name
        self.bank = bank
        self.image_path = f"bank_cards/{bank}_card.png"
        self.bal = 0.0
        self.availableBal = 0.0
        self.transactions = TransactionList()
        self.allTransactions = TransactionList()
        self.viewedTransactions = TransactionList()
        self.categories = []
        # static.logging.error(f"Created account {self.name} with {self.bank}")

    def getTransactionsByCategory(self, category_name):
        for category in self.categories:
            if category.name == category_name:
                return category.transactions
        return TransactionList()  # Return an empty list if the category is not found

    def openTransactions(self, inputFileName):
        try:
            with open(inputFileName, 'r', encoding='ISO-8859-1') as file:
                reader = csv.reader(file)
                lines = list(reader)
                if len(lines) < 3:
                    raise ValueError("CSV file too short to contain valid data.")
                self.bal = parseCurrency(lines[1][1])
                self.availableBal = parseCurrency(lines[2][1])
                self.transactions = TransactionList()  # Reset transactions list
                for row in lines[5:]:
                    transaction = self.processLine(row)
                    self.transactions.add(transaction)
                    # static.logging.error(f"Added transaction: {transaction.desc}, {transaction.date}, {transaction.amount}")
        except Exception as e:
            print(e)
            # static.logging.error(f"Error opening transactions: {e}")
        self.allTransactions = self.transactions
        self.viewedTransactions = self.transactions

    # Process each transaction line
    def processLine(self, row):
        transaction = Transaction(row[0], row[1], row[2], row[3], row[4], row[5])
        return transaction

    def getCatNames(self):
        listOfCatNames = []
        for category in self.categories:
            listOfCatNames.append(category.name)
        return listOfCatNames

    def getCat(self, name):
        for category in self.categories:
            if category.name == name:
                return category
        return "NO CATEGORY FOUND"

    # Add a new category
    def addCategory(self, category):
        if "OTHER" not in self.getCatNames():
            self.categories.append(Category("OTHER", self.transactions))
        else:
            self.getCat('OTHER').transactions = self.transactions
        self.categories.append(category)
        # static.logging.error(f"Added category: {category}")

    def __repr__(self):
        return f"Account(name={self.name}, bank={self.bank}, balance={self.bal}, availableBalance={self.availableBal}, transactions={self.transactions}, categories={self.categories})"


# BankAccounts class definition
class BankAccounts:
    def __init__(self):
        self.accounts = {}

    # Add a new account
    def add_account(self, name, bank):
        if name in self.accounts:
            raise ValueError(f"Account '{name}' already exists.")
        self.accounts[name] = Account(name, bank)
        # static.logging.error(f"Added account: {name}")

    # Get account by name
    def get_account(self, name):
        return self.accounts.get(name)

    # Get all accounts
    def all_accounts(self):
        return self.accounts

    # Get list of banks
    def banks(self):
        return [
            {"name": "nationwide", "display_name": "Nationwide"},
            {"name": "hsbc", "display_name": "HSBC"},
            {"name": "natwest", "display_name": "NatWest"},
            {"name": "lloyds", "display_name": "Lloyds"},
            {"name": "bank-of-scotland", "display_name": "Bank of Scotland"},
            {"name": "rbs", "display_name": "Royal Bank of Scotland"},
        ]

    def __repr__(self):
        return f"BankAccounts(accounts={self.accounts})"
