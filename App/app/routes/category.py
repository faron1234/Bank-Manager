from flask import Blueprint, render_template, request
from ..models import bank_accounts_list, TransactionList

bp = Blueprint('category', __name__)


# Flask route for displaying category.html page and its transactions
@bp.route('/category/<account_name>/<category_name>', methods=['GET', 'POST'])
def category(account_name, category_name):
    account = bank_accounts_list.get_account(account_name)
    if not account:
        #logging.error(f"Account not found: {account_name}")
        return "Account not found", 404

    if request.method == 'POST':
        keywords = request.form['keywords'].split(',')
        account.transactions = account.allTransactions.getSubset(*keywords)

    transactions = account.getTransactionsByCategory(category_name)
    if transactions is None:
        transactions = TransactionList()
    transactions.getSums()
    return render_template('category.html', account=account, category=category_name, transactions=transactions)