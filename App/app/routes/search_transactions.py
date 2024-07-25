from flask import Blueprint, render_template, request, jsonify
from ..models import bank_accounts_list, TransactionList

bp = Blueprint('search_transactions', __name__)


# Flask route for finding transactions based on search
@bp.route('/search_transactions/<account_name>', methods=['GET'])
def search_transactions(account_name):
    query = request.args.get('query', '').strip().lower().split()
    account = bank_accounts_list.get_account(account_name)
    if not account:
        return "Account not found", 404

    print("\n\n", account.allTransactions.getSubset(keywords=query), "\n\n")
    account.viewedTransactions = TransactionList(account.allTransactions.getSubset(keywords=query))
    transactions_html = render_template('transactions_table_rows.html', transactions=account.viewedTransactions.transactions)
    stats_html = render_template('transaction_stats.html', stats=account.viewedTransactions)

    return jsonify({
        'transactions': transactions_html,
        'stats': stats_html
    })