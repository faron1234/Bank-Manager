from datetime import datetime
from ...static import parseCurrency


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
