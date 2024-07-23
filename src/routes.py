from flask import Flask, render_template, request, jsonify
from src.models import BankAccounts, Category, TransactionList, static
# import logging

app = Flask(__name__)
bank_accounts = BankAccounts()

# Example data
bank_accounts.add_account('flexOne', 'nationwide')
bank_accounts.get_account('flexOne').openTransactions('statements/Statement Download 2024-Jul-10 14-57-29.csv')


# Flask template filter for displaying currency
@app.template_filter('currency')
def currency_filter(value):
    return f"£{value:,.2f}"


# Flask template filter for absolute value
@app.template_filter('abs')
def abs_filter(value):
    return abs(value)


# Flask route for index page
@app.route('/')
def index():
    return render_template('index.html', accounts=bank_accounts.all_accounts(), banks=bank_accounts.banks())


@app.route('/account/<name>', methods=['GET'])
def account(name):
    account = bank_accounts.get_account(name)
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
        account.allTransactions.sort(static.Sorts.dateSort, sort_direction)
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


@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    account_name = data.get('account_name', '').strip()
    bank = data.get('bank', '').strip()

    if not account_name or not bank:
        return jsonify({'error': 'Account name or bank is missing'}), 400

    try:
        bank_accounts.add_account(account_name, bank)
    except ValueError as e:
        # logging.error(f"Error creating account: {e}")
        return jsonify({'error': str(e)}), 400

    return jsonify({"message": "Account created", "account": account_name})


@app.route('/create_category', methods=['POST'])
def create_category():
    data = request.get_json()
    account_name = data.get('account')
    category_name = data.get('category')

    account = bank_accounts.get_account(account_name)
    if not account:
        # logging.error(f"Account not found: {account_name}")
        return jsonify({"error": "Account not found"}), 404

    newCategory = Category(category_name)
    account.addCategory(newCategory)
    # logging.debug(f"Category created: {category_name} in account {account_name}")

    return jsonify({"message": "Category created", "category": category_name})


@app.route('/add_keywords', methods=['POST'])
def add_keywords():
    data = request.json
    account_name = data.get('account')
    category_name = data.get('category')
    keywords = data.get('keywords').split(',')

    account = bank_accounts.get_account(account_name)
    if not account:
        #logging.error(f"Account not found: {account_name}")
        return jsonify({"error": "Account not found"}), 404

    category = account.get_category(category_name)
    if not category:
        #logging.error(f"Category not found: {category_name}")
        return jsonify({"error": "Category not found"}), 404

    category.addTransactions(account.transactions.getSubset(keywords))
    #logging.debug(f"Keywords added to category {category_name}: {keywords}")

    return jsonify({"message": "Keywords added", "keywords": keywords})


@app.route('/search_transactions/<account_name>', methods=['GET'])
def search_transactions(account_name):
    query = request.args.get('query', '').strip().lower().split()
    account = bank_accounts.get_account(account_name)
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


@app.route('/category/<account_name>/<category_name>', methods=['GET', 'POST'])
def category(account_name, category_name):
    account = bank_accounts.get_account(account_name)
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


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)