from . import TransactionList, Transaction, Category
from ...static import parseCurrency
import csv


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

    def hasTransactions(self):
        print(self.allTransactions.totalTransactions)
        if self.allTransactions.totalTransactions > 0:
            return True
        else:
            return False

    def __repr__(self):
        return f"Account(name={self.name}, bank={self.bank}, balance={self.bal}, availableBalance={self.availableBal}, transactions={self.transactions}, categories={self.categories})"
