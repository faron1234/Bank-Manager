from flask import Blueprint, request, render_template
from ..models import bank_accounts_list
from ...static import Sorts

bp = Blueprint('account', __name__)


# Flask route for displaying account.html and its transactions
@bp.route('/account/<name>', methods=['GET'])
def account(name):
    account = bank_accounts_list.get_account(name)
    if not account:
        # static.logging.error(f"Account not found: {name}")
        return "Account not found", 404

    sort_by = request.args.get('sort_by', '1')
    sort_direction = request.args.get('sort_direction', 'asc')

    if sort_by is not None:
        if sort_direction == 'asc':
            next_sort_direction = 'desc'
        else:
            next_sort_direction = 'asc'
        account.allTransactions.sort(int(sort_by), sort_direction)
    else:
        account.allTransactions.sort(Sorts.dateSort, sort_direction)
        next_sort_direction = 'desc'

    categories = [(category.name, len(category.transactions.transactions)) for category in account.categories]
    # static.logging.debug(f"Categories for account {name}: {categories}")

    account.allTransactions.getSums()
    stats = {
        "total_in": account.allTransactions.inSum,
        "total_out": account.allTransactions.outSum,
        "total_change": account.allTransactions.change,
        "total_transactions": account.allTransactions.amount()
    }

    return render_template('account.html', account=account, categories=categories, stats=stats, sort_by=sort_by, sort_direction=sort_direction, next_sort_direction=next_sort_direction)
