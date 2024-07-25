# BankAccounts class definition
class BankAccounts:
    def __init__(self):
        self.accounts = {}

    # Add a new account
    def add_account(self, name, bank):
        from ..models import Account
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
